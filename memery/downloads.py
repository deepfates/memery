"""Pure helpers for handing original search results out of the browser UI."""

from __future__ import annotations

from io import BytesIO
import mimetypes
from pathlib import Path
import zipfile


def file_download(path: str) -> tuple[bytes, str, str]:
    source = Path(path)
    mime = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
    return source.read_bytes(), source.name, mime


def results_archive(paths: list[str], root: str) -> bytes:
    """Return originals as a ZIP while retaining paths relative to the corpus."""
    corpus = Path(root).resolve()
    output = BytesIO()
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        used: set[str] = set()
        for value in paths:
            source = Path(value).resolve()
            try:
                name = str(source.relative_to(corpus))
            except ValueError:
                name = source.name
            if name in used:
                stem, suffix = Path(name).stem, Path(name).suffix
                index = 2
                while f"{stem}-{index}{suffix}" in used:
                    index += 1
                name = f"{stem}-{index}{suffix}"
            used.add(name)
            archive.writestr(name, source.read_bytes())
    return output.getvalue()
