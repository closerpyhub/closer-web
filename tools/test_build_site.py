"""Regression coverage for the public export boundary; no network."""

from __future__ import annotations

import contextlib
import io
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import build_site


class PublicExportTests(unittest.TestCase):
    def test_export_contains_every_public_page_and_excludes_workspace_material(self):
        with TemporaryDirectory() as temporary:
            output = Path(temporary) / "public"
            with patch.object(sys, "argv", ["build_site.py", "--output", str(output)]), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(build_site.main(), 0)

            expected_pages = {path.name for path in build_site.ROOT.glob("*.html")}
            exported_pages = {path.name for path in output.glob("*.html")}
            self.assertEqual(exported_pages, expected_pages)
            self.assertTrue((output / "assets" / "clients" / "copetrol.webp").is_file())
            for private_path in ("work", "materials", "tools", "README.md", "Desechos"):
                self.assertFalse((output / private_path).exists(), private_path)


if __name__ == "__main__":
    unittest.main()
