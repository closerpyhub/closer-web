"""Regression coverage for the destination guard; no credentials or network."""

import copy
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from check_hosting import ACCOUNT_ID, BRANCH, DOMAINS, PROJECT_ID, PROJECT_NAME, read_target, validate_target, verify_public


class DestinationTests(unittest.TestCase):
    def setUp(self):
        self.project = {
            "id": PROJECT_ID, "name": PROJECT_NAME, "production_branch": BRANCH,
            "domains": list(DOMAINS), "source": {"config": {"deployments_enabled": False}},
            "canonical_deployment": {
                "environment": "production", "latest_stage": {"status": "success"},
                "deployment_trigger": {"metadata": {"commit_hash": "expected-sha"}},
            },
        }

    def test_correct_destination_and_release(self):
        validate_target(self.project, "expected-sha")

    def test_wrong_project_branch_or_missing_domain(self):
        for key, value in [("id", "other-project"), ("name", "other-site"),
                           ("production_branch", "main"), ("domains", ["other.example"])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_target({**self.project, key: value})

    def test_obsolete_git_publisher_must_be_disabled(self):
        for source in [{}, {"config": {"deployments_enabled": True}}]:
            with self.subTest(source=source), self.assertRaises(ValueError):
                validate_target({**self.project, "source": source})

    def test_preview_failed_or_old_production_is_rejected(self):
        for key, value in [("environment", "preview"), ("latest_stage", {"status": "failure"}),
                           ("deployment_trigger", {"metadata": {"commit_hash": "old-sha"}})]:
            project = copy.deepcopy(self.project)
            project["canonical_deployment"][key] = value
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate_target(project, "expected-sha")

    def test_wrong_account_fails_before_network(self):
        with patch.dict("os.environ", {"CLOUDFLARE_ACCOUNT_ID": "other-account"}, clear=True), \
                patch("check_hosting.urlopen") as request, self.assertRaises(ValueError):
            read_target()
        request.assert_not_called()

    def test_missing_token_fails_before_network(self):
        with patch.dict("os.environ", {"CLOUDFLARE_ACCOUNT_ID": ACCOUNT_ID}, clear=True), \
                patch("check_hosting.urlopen") as request, self.assertRaises(ValueError):
            read_target()
        request.assert_not_called()

    def test_old_html_with_the_same_title_and_assets_is_rejected(self):
        with TemporaryDirectory() as temporary:
            directory = Path(temporary)
            directory.joinpath("index.html").write_text(
                '<title>Closer</title><meta name="closer-release" content="new-sha">'
                '<link href="styles.css?v=123"><script src="script.js?v=123"></script>', encoding="utf-8"
            )
            directory.joinpath("styles.css").write_text("body{}", encoding="utf-8")
            directory.joinpath("script.js").write_text("'use strict';", encoding="utf-8")
            directory.joinpath("sitemap.xml").write_text("<urlset/>", encoding="utf-8")

            def stale_response(url):
                relative = url.split(".py", 1)[1].split("?", 1)[0].lstrip("/") or "index.html"
                return directory.joinpath(relative).read_bytes().replace(b"new-sha", b"old-sha")

            with patch("check_hosting.fetch_public", side_effect=stale_response), self.assertRaises(ValueError):
                verify_public(directory, "new-sha")


if __name__ == "__main__":
    unittest.main()
