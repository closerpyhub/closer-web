"""Fail closed on the Pages destination; verify the public release without writes."""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit
from urllib.request import Request, urlopen


ACCOUNT_ID = "60706308dfe00ad618d8baf5fd4fe001"
PROJECT_ID = "089d08e6-cefa-4d17-91f0-a15571346a43"
PROJECT_NAME = "closer-web"
BRANCH = "master"
DOMAINS = ("closer.com.py", "www.closer.com.py")


def validate_target(project: dict, expected_commit: str | None = None) -> None:
    if (project.get("id"), project.get("name"), project.get("production_branch")) != (
        PROJECT_ID, PROJECT_NAME, BRANCH
    ):
        raise ValueError("Pages project or production branch does not match WEB Closer")
    if not set(DOMAINS).issubset(project.get("domains", [])):
        raise ValueError("WEB Closer production domains are not assigned to this project")
    if project.get("source", {}).get("config", {}).get("deployments_enabled") is not False:
        raise ValueError("Disable the obsolete native Git publisher before using Actions")
    if expected_commit:
        release = project.get("canonical_deployment") or {}
        commit = release.get("deployment_trigger", {}).get("metadata", {}).get("commit_hash")
        if (release.get("environment"), release.get("latest_stage", {}).get("status"), commit) != (
            "production", "success", expected_commit
        ):
            raise ValueError("Production does not contain the expected successful source commit")


def read_target() -> dict:
    if os.environ.get("CLOUDFLARE_ACCOUNT_ID") != ACCOUNT_ID:
        raise ValueError("Cloudflare account does not match WEB Closer")
    token = os.environ.get("CLOUDFLARE_API_TOKEN")
    if not token:
        raise ValueError("Cloudflare Pages deployment credential is missing")
    request = Request(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}",
        headers={"Authorization": f"Bearer {token}", "User-Agent": "closer-web-deploy-check"},
    )
    with urlopen(request, timeout=30) as response:
        document = json.load(response)
    if not document.get("success"):
        raise ValueError("Cloudflare did not confirm the Pages project")
    return document["result"]


def fetch_public(url: str) -> bytes:
    request = Request(url, headers={"Cache-Control": "no-cache", "User-Agent": "closer-web-deploy-check"})
    with urlopen(request, timeout=30) as response:
        # A redirect to another project/account must not be accepted as success.
        if response.status != 200 or urlsplit(response.url).netloc != urlsplit(url).netloc:
            raise ValueError("Public release returned an unexpected status or host")
        return response.read()


def verify_public(directory: Path, expected_commit: str) -> None:
    local_html = (directory / "index.html").read_text(encoding="utf-8-sig")
    references = re.findall(r'(?:src|href)=["\']((?:styles\.css|script\.js)\?v=[^"\']+)["\']', local_html)
    if len(set(references)) != 2:
        raise ValueError("Export must contain the versioned site stylesheet and script")
    marker = f'<meta name="closer-release" content="{expected_commit}">'
    if marker not in local_html:
        raise ValueError("Export does not contain the expected source commit marker")
    for domain in DOMAINS:
        origin = f"https://{domain}"
        remote_html = fetch_public(origin + "/").decode("utf-8-sig")
        # Cloudflare inserts analytics and email protection into HTML; do not
        # require byte equality or disable these protections to make a check pass.
        title = re.search(r"<title>.*?</title>", local_html, re.S)
        if not title or title.group() not in remote_html or marker not in remote_html or any(ref not in remote_html for ref in references):
            raise ValueError(f"{domain} does not serve the expected WEB Closer release")
        for artifact in sorted(directory.rglob("*")):
            if not artifact.is_file() or artifact.name == "index.html":
                continue
            relative = artifact.relative_to(directory).as_posix()
            route = relative[:-5] if artifact.suffix == ".html" else relative
            public = fetch_public(f"{origin}/{route}")
            if artifact.suffix == ".html":
                if marker not in public.decode("utf-8-sig"):
                    raise ValueError(f"Public HTML has an old/missing release marker: {domain}/{relative}")
            elif relative == "robots.txt":
                # The managed Cloudflare crawl policy is intentionally preserved.
                if artifact.read_text(encoding="utf-8-sig").strip() not in public.decode("utf-8-sig"):
                    raise ValueError(f"Public robots.txt does not contain the source policy: {domain}")
            elif public != artifact.read_bytes():
                raise ValueError(f"Public artifact differs from the export: {domain}/{relative}")
        print(f"PASS: {domain} serves all exported artifacts and HTML release {expected_commit}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--commit", help="Expected production source SHA after deployment")
    parser.add_argument("--public-dir", type=Path, help="Export to compare against the public domains")
    args = parser.parse_args()
    try:
        if args.public_dir and not args.commit:
            raise ValueError("Public release verification requires the expected source commit")
        validate_target(read_target(), args.commit)
        print(f"PASS: Pages {ACCOUNT_ID}/{PROJECT_NAME}, branch {BRANCH}, production domains")
        if args.public_dir:
            verify_public(args.public_dir, args.commit)
    except (OSError, ValueError, HTTPError) as error:
        # Do not dump provider responses, request headers or credentials.
        print(f"FAIL: {type(error).__name__}: {error}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
