"""Export only public website files into a new directory, without dependencies."""

from __future__ import annotations

import argparse
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit

from check_site import ROOT, Page, main as check_site


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='New or empty output directory; defaults to a temporary directory.')
    args = parser.parse_args()
    if check_site():
        return 1

    html_files = sorted(ROOT.glob('*.html'))
    files = set(html_files) | {ROOT / name for name in ('styles.css', 'script.js', 'robots.txt', 'sitemap.xml')}

    def add_asset(reference: str) -> None:
        url = urlsplit(reference)
        if url.scheme or url.netloc:
            return
        relative = unquote(url.path).lstrip('/')
        if not relative:
            return
        target = (ROOT / relative).resolve()
        if not target.is_relative_to(ROOT / 'assets'):
            return
        if not target.is_file():
            raise ValueError(f'Missing asset: {relative}')
        files.add(target)

    for path in html_files:
        for reference, _line in Page(path).references:
            add_asset(reference)
    css = (ROOT / 'styles.css').read_text(encoding='utf-8-sig')
    for reference in re.findall(r'url\(\s*[\"\']?([^\"\')]+)[\"\']?\s*\)', css):
        add_asset(reference)
    files.add(ROOT / 'assets/fonts/OFL.txt')

    output = args.output.resolve() if args.output else Path(tempfile.mkdtemp(prefix='closer-web-public-'))
    if output == ROOT or ROOT.is_relative_to(output):
        raise ValueError('Output must not be the repository or one of its parent directories.')
    if output.exists() and any(output.iterdir()):
        raise ValueError(f'Output must be empty; no files were removed: {output}')
    output.mkdir(parents=True, exist_ok=True)
    for source in sorted(files):
        destination = output / source.relative_to(ROOT)
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)

    print(f'Exported {len(files)} public files ({sum(path.stat().st_size for path in files)} bytes).')
    print(f'PUBLIC_SITE_DIR={output}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
