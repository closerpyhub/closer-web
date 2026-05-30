from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
}


def clean(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as zf:
        xml = zf.read("word/document.xml")
    root = ET.fromstring(xml)
    blocks: list[str] = []
    for para in root.findall(".//w:p", NS):
        pieces = []
        for node in para.iter():
            if node.tag == f"{{{NS['w']}}}t" and node.text:
                pieces.append(node.text)
            elif node.tag == f"{{{NS['w']}}}tab":
                pieces.append("\t")
            elif node.tag == f"{{{NS['w']}}}br":
                pieces.append("\n")
        line = clean("".join(pieces))
        if line:
            blocks.append(line)
    return "\n".join(blocks)


def shared_strings(zf: zipfile.ZipFile) -> list[str]:
    try:
        xml = zf.read("xl/sharedStrings.xml")
    except KeyError:
        return []
    root = ET.fromstring(xml)
    out = []
    for si in root.findall(".//a:si", NS):
        text = "".join(t.text or "" for t in si.findall(".//a:t", NS))
        out.append(clean(text))
    return out


def xlsx_text(path: Path) -> str:
    lines: list[str] = []
    with zipfile.ZipFile(path) as zf:
        strings = shared_strings(zf)
        sheets = sorted(name for name in zf.namelist() if name.startswith("xl/worksheets/sheet") and name.endswith(".xml"))
        for sheet_name in sheets:
            lines.append(f"## {sheet_name}")
            root = ET.fromstring(zf.read(sheet_name))
            for row in root.findall(".//a:row", NS):
                cells = []
                for cell in row.findall("a:c", NS):
                    value = cell.find("a:v", NS)
                    if value is None or value.text is None:
                        inline = "".join(t.text or "" for t in cell.findall(".//a:t", NS))
                        cells.append(clean(inline))
                        continue
                    if cell.attrib.get("t") == "s":
                        idx = int(value.text)
                        cells.append(strings[idx] if idx < len(strings) else "")
                    else:
                        cells.append(clean(value.text))
                row_text = " | ".join(item for item in cells if item)
                if row_text:
                    lines.append(row_text)
    return "\n".join(lines)


def pdf_text(path: Path) -> str:
    try:
        from pypdf import PdfReader
    except Exception as exc:  # pragma: no cover
        return f"[No se pudo importar pypdf: {exc}]"

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"\n{3,}", "\n\n", text).strip()
        if text:
            pages.append(f"## Pagina {i}\n{text}")
    return "\n\n".join(pages)


def image_info(path: Path) -> dict[str, object]:
    try:
        from PIL import Image
    except Exception:
        return {"file": path.name, "error": "Pillow no disponible"}
    with Image.open(path) as img:
        return {"file": path.name, "width": img.width, "height": img.height, "mode": img.mode}


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: extract_materials.py <source_dir> <output_dir>", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    output = Path(sys.argv[2])
    output.mkdir(parents=True, exist_ok=True)

    extracted: dict[str, str] = {}
    images: list[dict[str, object]] = []

    for path in sorted(source.iterdir(), key=lambda p: p.name.lower()):
        suffix = path.suffix.lower()
        if suffix == ".docx":
            extracted[path.name] = docx_text(path)
        elif suffix == ".xlsx":
            extracted[path.name] = xlsx_text(path)
        elif suffix == ".pdf":
            extracted[path.name] = pdf_text(path)
        elif suffix in {".png", ".jpg", ".jpeg", ".webp"}:
            images.append(image_info(path))
        elif path.is_file() and path.stat().st_size:
            extracted[path.name] = path.read_text(encoding="utf-8", errors="replace")

    combined_parts = []
    for name, text in extracted.items():
        out_path = output / f"{name}.txt"
        out_path.write_text(text, encoding="utf-8")
        combined_parts.append(f"# {name}\n{text}")

    (output / "combined_text.txt").write_text("\n\n".join(combined_parts), encoding="utf-8")
    (output / "image_inventory.json").write_text(json.dumps(images, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"documents": list(extracted), "images": images}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
