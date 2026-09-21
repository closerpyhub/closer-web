"""Check routes, local references, metadata, structured data and crawl files.

Run from any directory with: python tools/check_site.py
Uses only the Python standard library; does not fetch URLs or execute JavaScript.
"""

from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree


ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://closer.com.py"
REQUIRED_ROUTES = {
    "index.html", "index-opcion-servicios-clara.html", "contacto.html",
    "gestion-redes.html", "meta-ads.html", "chatbots-ia.html", "paginas-web.html",
    "apps-sistemas.html", "campanias-creativas.html", "google-ads.html",
    "automatizaciones-bi.html", "plan-redes-presencia.html",
    "plan-redes-impulso.html", "plan-redes-dominio.html", "plan-chatbot-ia.html",
    "plan-chatbots-atencion-inteligente.html", "plan-chatbots-optimizacion.html",
    "plan-chatbots-robot-avanzado.html", "plan-google-ads-inversion.html",
    "plan-google-ads-modulo.html", "plan-automatizacion-bi.html",
    "plan-automatizacion-mailing.html", "plan-automatizacion-manychat.html",
    "plan-campana-creativa-completa.html",
}
NOINDEX_ROUTES = {
    "index-opcion-servicios-clara.html", "plan-chatbots-atencion-inteligente.html",
    "plan-chatbots-optimizacion.html", "plan-chatbots-robot-avanzado.html",
}
SERVICE_ROUTES = REQUIRED_ROUTES - {"index.html", "contacto.html", "index-opcion-servicios-clara.html"}


def canonical_for(path: Path) -> str:
    return ORIGIN + ("/" if path.name == "index.html" else "/" + path.stem)


def local_target(url: str) -> Path | None:
    """Resolve a public URL to a local file; schema entity fragments are separate."""
    parsed = urlsplit(url)
    if parsed.netloc != "closer.com.py":
        return None
    target = (ROOT / unquote(parsed.path).lstrip("/")).resolve()
    if target.is_dir():
        target = target / "index.html"
    elif not target.suffix:
        # Cloudflare Pages redirects public .html URLs to their clean route.
        target = target.with_suffix(".html")
    return target if target.is_relative_to(ROOT) else None


class Page(HTMLParser):
    def __init__(self, path: Path) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: Counter[str] = Counter()
        self.text: dict[str, list[str]] = {"title": [], "h1": []}
        self.active_text: set[str] = set()
        self.descriptions: list[str] = []
        self.metadata: dict[str, list[str]] = defaultdict(list)
        self.canonicals: list[str] = []
        self.jsonld: list[str] = []
        self.in_jsonld = False
        self.references: list[tuple[str, int]] = []
        self.feed(path.read_text(encoding="utf-8-sig"))
        self.close()

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids[attributes["id"] or ""] += 1
        if tag in self.text:
            self.text[tag].append("")
            self.active_text.add(tag)
        if tag == "meta":
            key = (attributes.get("name") or attributes.get("property") or "").lower()
            if key:
                self.metadata[key].append(attributes.get("content") or "")
            if key == "description":
                self.descriptions.append(attributes.get("content") or "")
        if tag == "link" and "canonical" in (attributes.get("rel") or "").lower().split():
            self.canonicals.append(attributes.get("href") or "")
        if tag == "script" and (attributes.get("type") or "").lower() == "application/ld+json":
            self.in_jsonld = True
            self.jsonld.append("")
        for name in ("href", "src"):
            if name in attributes:
                self.references.append((attributes[name] or "", self.getpos()[0]))

    def handle_endtag(self, tag: str) -> None:
        self.active_text.discard(tag)
        if tag == "script":
            self.in_jsonld = False

    def handle_data(self, data: str) -> None:
        if self.in_jsonld:
            self.jsonld[-1] += data
        for tag in self.active_text:
            self.text[tag][-1] += data


def check_metadata(path: Path, page: Page, errors: list[str]) -> None:
    canonical = canonical_for(path)
    if page.canonicals != [canonical]:
        errors.append(f"{path.name}: expected one canonical equal to {canonical}")
    for key, values in page.metadata.items():
        if len(values) != 1 or not values[0].strip():
            errors.append(f"{path.name}: duplicate or empty {key} metadata")
    expected = {
        "og:title": page.text["title"][0].strip() if page.text["title"] else "",
        "og:description": page.descriptions[0] if page.descriptions else "",
        "og:url": canonical,
        "og:type": "website",
        "og:site_name": "Closer",
        "twitter:card": "summary_large_image",
    }
    for key, value in expected.items():
        if page.metadata.get(key) != [value]:
            errors.append(f"{path.name}: {key} is missing or inconsistent with page metadata")
    for key, source in (("twitter:title", "og:title"), ("twitter:description", "og:description")):
        if key in page.metadata and page.metadata[key] != page.metadata.get(source):
            errors.append(f"{path.name}: {key} does not match {source}")
    robots = page.metadata.get("robots", [])
    directives = {item.strip().lower() for item in robots[0].split(",")} if len(robots) == 1 else set()
    required = {"noindex", "follow"} if path.name in NOINDEX_ROUTES else {"index", "follow", "max-image-preview:large"}
    forbidden = {"index", "nofollow", "none"} if path.name in NOINDEX_ROUTES else {"noindex", "nofollow", "none"}
    if not required.issubset(directives) or directives & forbidden:
        errors.append(f"{path.name}: incorrect robots metadata for its indexing policy")
    for key in ("og:image", "twitter:image"):
        values = page.metadata.get(key, [])
        if key == "og:image" and not values:
            errors.append(f"{path.name}: missing og:image")
        for value in values:
            try:
                target = local_target(value)
                valid = value.startswith(ORIGIN + "/") and target is not None and target.is_file()
            except ValueError:
                valid = False
            if not valid:
                errors.append(f"{path.name}: {key} must reference an existing HTTPS site image")
    if not page.metadata.get("og:image:alt"):
        errors.append(f"{path.name}: missing og:image:alt")


def objects(value: object):
    """Walk JSON objects, including nested schema references and list items."""
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from objects(child)
    elif isinstance(value, list):
        for child in value:
            yield from objects(child)


def check_structured_data(path: Path, page: Page, errors: list[str]) -> int:
    if len(page.jsonld) != 1:
        errors.append(f"{path.name}: expected one JSON-LD @graph")
        return 0
    try:
        document = json.loads(page.jsonld[0])
    except (ValueError, TypeError) as error:
        errors.append(f"{path.name}: invalid JSON-LD: {error}")
        return 0
    if not isinstance(document, dict) or document.get("@context") not in ("https://schema.org", "https://schema.org/"):
        errors.append(f"{path.name}: JSON-LD needs the schema.org context")
        return 0
    graph = document.get("@graph")
    if not isinstance(graph, list) or not graph or not all(isinstance(node, dict) for node in graph):
        errors.append(f"{path.name}: JSON-LD @graph must be a nonempty list of objects")
        return 0
    types: dict[str, list[dict]] = defaultdict(list)
    declared_ids: Counter[str] = Counter()
    for node in objects(graph):
        node_types = node.get("@type", [])
        if isinstance(node_types, str):
            node_types = [node_types]
        if not isinstance(node_types, list) or not all(isinstance(kind, str) for kind in node_types):
            errors.append(f"{path.name}: invalid JSON-LD @type")
            continue
        for kind in node_types:
            types[kind].append(node)
        if node_types and isinstance(node.get("@id"), str):
            declared_ids[node["@id"]] += 1
    required_types = {"Organization", "WebSite", "WebPage"}
    if path.name != "index.html":
        required_types.add("BreadcrumbList")
    if path.name in SERVICE_ROUTES:
        required_types.add("Service")
    for kind in sorted(required_types):
        if len(types[kind]) != 1:
            errors.append(f"{path.name}: expected one JSON-LD {kind}, found {len(types[kind])}")
    for identifier, count in declared_ids.items():
        if count > 1:
            errors.append(f"{path.name}: duplicate JSON-LD definition {identifier!r}")
    for node in types["WebPage"]:
        if node.get("url") != canonical_for(path):
            errors.append(f"{path.name}: JSON-LD WebPage URL differs from canonical")
    for node in objects(graph):
        for key in ("@id", "url", "item", "logo", "image", "contentUrl"):
            value = node.get(key)
            if value is None or isinstance(value, (dict, list)):
                continue
            if not isinstance(value, str):
                errors.append(f"{path.name}: JSON-LD {key} must be a URL or object")
                continue
            try:
                parsed = urlsplit(value)
                if not parsed.scheme or not parsed.netloc:
                    errors.append(f"{path.name}: JSON-LD {key} is not an absolute URL: {value!r}")
                    continue
                if parsed.netloc != "closer.com.py":
                    continue
                target = local_target(value)
                if parsed.scheme != "https" or target is None or not target.is_file():
                    errors.append(f"{path.name}: unresolved local JSON-LD URL {value!r}")
                if key == "@id" and value not in declared_ids:
                    errors.append(f"{path.name}: JSON-LD reference has no entity definition: {value!r}")
            except ValueError:
                errors.append(f"{path.name}: malformed JSON-LD URL {value!r}")
    return len(graph)


def check_crawl_files(paths: list[Path], errors: list[str]) -> int:
    expected_urls = {canonical_for(path) for path in paths if path.name not in NOINDEX_ROUTES}
    sitemap_urls: list[str] = []
    try:
        sitemap = ElementTree.parse(ROOT / "sitemap.xml").getroot()
        namespace = "{http://www.sitemaps.org/schemas/sitemap/0.9}"
        if sitemap.tag != namespace + "urlset":
            errors.append("sitemap.xml: expected a sitemap urlset with the standard namespace")
        for entry in sitemap.findall(namespace + "url"):
            locations = entry.findall(namespace + "loc")
            if len(locations) != 1 or not (locations[0].text or "").strip():
                errors.append("sitemap.xml: each URL must have one nonempty loc")
            else:
                sitemap_urls.append(locations[0].text.strip())
        if len(sitemap_urls) != len(set(sitemap_urls)):
            errors.append("sitemap.xml: duplicate URLs")
        for url in sorted(expected_urls - set(sitemap_urls)):
            errors.append(f"sitemap.xml: missing indexable canonical {url}")
        for url in sorted(set(sitemap_urls) - expected_urls):
            errors.append(f"sitemap.xml: unexpected or noindex URL {url}")
    except (OSError, ElementTree.ParseError) as error:
        errors.append(f"sitemap.xml: {error}")

    try:
        lines = (ROOT / "robots.txt").read_text(encoding="utf-8-sig").splitlines()
    except (OSError, UnicodeError) as error:
        errors.append(f"robots.txt: {error}")
        return len(sitemap_urls)
    rules: list[tuple[str, str]] = []
    agents: list[str] = []
    saw_rule = False
    sitemap_directives: list[str] = []
    for line in lines:
        field, separator, value = line.split("#", 1)[0].partition(":")
        if not separator:
            continue
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if saw_rule:
                agents = []
                saw_rule = False
            agents.append(value.lower())
        elif field in {"allow", "disallow"}:
            saw_rule = True
            if "*" in agents and value:
                rules.append((field, value))
        elif field == "sitemap":
            sitemap_directives.append(value)
    if ("allow", "/") not in rules:
        errors.append("robots.txt: expected Allow: / for User-agent: *")
    if sitemap_directives != [ORIGIN + "/sitemap.xml"]:
        errors.append("robots.txt: expected one public sitemap URL")

    def allowed(url_path: str) -> bool:
        # Crawlers use the most specific matching rule; Allow wins equal lengths.
        matches = []
        for action, pattern in rules:
            anchored = pattern.endswith("$")
            body = pattern[:-1] if anchored else pattern
            expression = "^" + re.escape(body).replace(r"\*", ".*") + ("$" if anchored else "")
            if re.search(expression, url_path):
                matches.append((len(body.replace("*", "")), action == "allow"))
        return max(matches)[1] if matches else True

    public_paths = {urlsplit(canonical_for(path)).path for path in paths}
    public_paths.update("/" + path.name for path in ROOT.glob("*.css"))
    public_paths.update("/" + path.name for path in ROOT.glob("*.js"))
    public_paths.update("/" + path.relative_to(ROOT).as_posix() for path in (ROOT / "assets").rglob("*") if path.is_file())
    for url_path in sorted(public_paths):
        if not allowed(url_path):
            errors.append(f"robots.txt: blocks a public page or resource: {url_path}")
    for url_path in ("/materials/combined_text.txt", "/tools/check_site.py", "/.git/config", "/README.md"):
        if allowed(url_path):
            errors.append(f"robots.txt: missing exclusion for {url_path}")
    return len(sitemap_urls)


def main() -> int:
    errors: list[str] = []
    paths = sorted(ROOT.glob("*.html"))
    pages: dict[Path, Page] = {}
    schema_nodes = 0
    unique_metadata: dict[str, dict[str, list[str]]] = {
        "title": defaultdict(list), "description": defaultdict(list),
    }
    missing = REQUIRED_ROUTES - {path.name for path in paths}
    for name in sorted(missing):
        errors.append(f"Missing required route: {name}")

    for path in paths:
        try:
            page = Page(path)
        except (OSError, UnicodeError) as error:
            errors.append(f"{path.name}: could not read HTML: {error}")
            continue
        pages[path.resolve()] = page
        for tag, values in page.text.items():
            if len(values) != 1 or not values[0].strip():
                errors.append(f"{path.name}: expected one nonempty <{tag}>, found {len(values)}")
        if len(page.descriptions) != 1 or not page.descriptions[0].strip():
            errors.append(f"{path.name}: expected one nonempty meta description")
        for key, values in (("title", page.text["title"]), ("description", page.descriptions)):
            if len(values) == 1:
                normalized = " ".join(values[0].split()).casefold()
                unique_metadata[key][normalized].append(path.name)
        check_metadata(path, page, errors)
        schema_nodes += check_structured_data(path, page, errors)
        for identifier, count in page.ids.items():
            if not identifier or count > 1:
                errors.append(f"{path.name}: invalid or duplicate id {identifier!r} ({count} occurrences)")

    for key, values in unique_metadata.items():
        for names in values.values():
            if len(names) > 1:
                errors.append(f"Duplicate {key}: {', '.join(names)}")

    references = 0
    fragments = 0
    for path, page in list(pages.items()):
        for reference, line in page.references:
            location = f"{path.name}:{line}"
            try:
                url = urlsplit(reference.strip())
            except ValueError:
                errors.append(f"{location}: malformed URL {reference!r}")
                continue
            if url.scheme or url.netloc:
                continue
            references += 1
            if not reference.strip():
                errors.append(f"{location}: empty local reference")
                continue
            relative = unquote(url.path)
            target = path if not relative else (
                ROOT / relative.lstrip("/") if relative.startswith("/") else path.parent / relative
            )
            target = target.resolve()
            if not target.is_relative_to(ROOT):
                errors.append(f"{location}: local reference leaves site root: {reference!r}")
                continue
            if target.is_dir():
                target = target / "index.html"
            if not target.is_file():
                errors.append(f"{location}: missing local target {reference!r}")
                continue
            if url.fragment and target.suffix.lower() == ".html":
                fragments += 1
                if target not in pages:
                    try:
                        pages[target] = Page(target)
                    except (OSError, UnicodeError) as error:
                        errors.append(f"{location}: cannot read fragment target: {error}")
                        continue
                if unquote(url.fragment) not in pages[target].ids:
                    errors.append(f"{location}: missing fragment {reference!r}")

    sitemap_count = check_crawl_files(paths, errors)
    status = "FAIL" if errors else "PASS"
    print(f"{status}: {len(paths)} pages, {references} local references, {fragments} fragments, "
          f"{schema_nodes} schema nodes, {sitemap_count} sitemap URLs, {len(errors)} errors.")
    for error in errors:
        print(f"  - {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
