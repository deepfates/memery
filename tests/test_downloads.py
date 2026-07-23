from io import BytesIO
from pathlib import Path
import zipfile

from memery.downloads import file_download, results_archive


def test_file_download_returns_original_bytes_name_and_mime(tmp_path: Path):
    image = tmp_path / "result.png"
    image.write_bytes(b"original image bytes")

    assert file_download(str(image)) == (
        b"original image bytes",
        "result.png",
        "image/png",
    )


def test_results_archive_preserves_relative_paths(tmp_path: Path):
    first = tmp_path / "first" / "same.jpg"
    second = tmp_path / "second" / "same.jpg"
    first.parent.mkdir()
    second.parent.mkdir()
    first.write_bytes(b"first")
    second.write_bytes(b"second")

    payload = results_archive([str(first), str(second)], str(tmp_path))

    with zipfile.ZipFile(BytesIO(payload)) as archive:
        assert archive.namelist() == ["first/same.jpg", "second/same.jpg"]
        assert archive.read("first/same.jpg") == b"first"
        assert archive.read("second/same.jpg") == b"second"
