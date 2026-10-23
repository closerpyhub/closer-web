"""Regression coverage for editorial route validation; no network or dependencies."""

from __future__ import annotations

import contextlib
import io
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import check_site


class EditorialRouteTests(unittest.TestCase):
    def setUp(self):
        self.temporary = TemporaryDirectory()
        self.root = Path(self.temporary.name)
        (self.root / "assets" / "brand").mkdir(parents=True)
        (self.root / "assets" / "brand" / "image.webp").write_bytes(b"image")
        (self.root / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nDisallow: /materials/\nDisallow: /tools/\nDisallow: /.git/\nDisallow: /README.md\n"
            "Sitemap: https://closer.com.py/sitemap.xml\n",
            encoding="utf-8",
        )

    def tearDown(self):
        self.temporary.cleanup()

    def write_page(self, name: str, *, article: bool = False, service: bool = False,
                   og_type: str | None = None, include_article: bool = True,
                   broken_article_reference: bool = False) -> None:
        canonical = check_site.ORIGIN + ("/" if name == "index.html" else f"/{Path(name).stem}")
        page_id = f"{canonical}#webpage"
        article_id = f"{canonical}#article"
        graph = [
            {"@type": "Organization", "@id": f"{check_site.ORIGIN}/#organization", "url": check_site.ORIGIN + "/"},
            {"@type": "WebSite", "@id": f"{check_site.ORIGIN}/#website", "url": check_site.ORIGIN + "/"},
            {"@type": "WebPage", "@id": page_id, "url": canonical},
        ]
        if name != "index.html":
            graph.append({"@type": "BreadcrumbList", "@id": f"{canonical}#breadcrumb", "itemListElement": []})
        if service:
            graph.append({"@type": "Service", "@id": f"{canonical}#service", "name": "Servicio", "url": canonical})
        if include_article:
            graph[2]["mainEntity"] = {"@id": f"{canonical}#missing" if broken_article_reference else article_id}
            graph.append({
                "@type": "Article", "@id": article_id, "headline": "Guía útil", "description": "Una guía útil.",
                "url": canonical, "mainEntityOfPage": {"@id": page_id},
                "author": {"@id": f"{check_site.ORIGIN}/#organization"},
                "publisher": {"@id": f"{check_site.ORIGIN}/#organization"},
            })
        expected_og_type = og_type or ("article" if article else "website")
        title = "Guía útil" if article else "Inicio"
        description = "Una guía útil." if article else "La portada del sitio."
        html = f'''<!doctype html><html lang="es-PY"><head>
<title>{title}</title><meta name="description" content="{description}">
<meta name="robots" content="index, follow, max-image-preview:large"><link rel="canonical" href="{canonical}">
<meta property="og:type" content="{expected_og_type}"><meta property="og:site_name" content="Closer">
<meta property="og:title" content="{title}"><meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}"><meta property="og:image" content="{check_site.ORIGIN}/assets/brand/image.webp">
<meta property="og:image:alt" content="Imagen de prueba"><meta name="twitter:card" content="summary_large_image">
<script type="application/ld+json">{json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)}</script>
</head><body><main><h1>{title}</h1></main></body></html>'''
        (self.root / name).write_text(html, encoding="utf-8")

    def write_sitemap(self, *names: str) -> None:
        urls = "".join(
            f"<url><loc>{check_site.ORIGIN}{'/' if name == 'index.html' else '/' + Path(name).stem}</loc></url>"
            for name in names
        )
        (self.root / "sitemap.xml").write_text(
            f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>',
            encoding="utf-8",
        )

    def run_checker(self, *, required: set[str], services: set[str], articles: set[str], noindex: set[str] | None = None) -> int:
        with patch.object(check_site, "ROOT", self.root), \
             patch.object(check_site, "REQUIRED_ROUTES", required), \
             patch.object(check_site, "SERVICE_ROUTES", services), \
             patch.object(check_site, "ARTICLE_ROUTES", articles), \
             patch.object(check_site, "NOINDEX_ROUTES", noindex or set()), \
             contextlib.redirect_stdout(io.StringIO()):
            return check_site.main()

    def test_article_route_accepts_article_graph_and_article_og_type(self):
        self.write_page("index.html")
        self.write_page("guia.html", article=True)
        self.write_sitemap("index.html", "guia.html")

        self.assertEqual(self.run_checker(
            required={"index.html", "guia.html"}, services=set(), articles={"guia.html"},
        ), 0)

    def test_article_route_rejects_website_og_type(self):
        self.write_page("index.html")
        self.write_page("guia.html", article=True, og_type="website")
        self.write_sitemap("index.html", "guia.html")

        self.assertEqual(self.run_checker(
            required={"index.html", "guia.html"}, services=set(), articles={"guia.html"},
        ), 1)

    def test_article_route_rejects_missing_or_broken_article_entity(self):
        self.write_page("index.html")
        self.write_page("guia.html", article=True, include_article=False)
        self.write_sitemap("index.html", "guia.html")

        self.assertEqual(self.run_checker(
            required={"index.html", "guia.html"}, services=set(), articles={"guia.html"},
        ), 1)

        self.write_page("guia.html", article=True, broken_article_reference=True)
        self.assertEqual(self.run_checker(
            required={"index.html", "guia.html"}, services=set(), articles={"guia.html"},
        ), 1)

    def test_service_route_still_requires_service_schema(self):
        self.write_page("index.html")
        self.write_page("servicio.html")
        self.write_sitemap("index.html", "servicio.html")

        self.assertEqual(self.run_checker(
            required={"index.html", "servicio.html"}, services={"servicio.html"}, articles=set(),
        ), 1)


if __name__ == "__main__":
    unittest.main()
