import shutil
from pathlib import Path


def clear_dir(path):
    path = Path(path)
    if path.exists():
        for file in path.iterdir():
            if file.is_dir():
                shutil.rmtree(file)
            else:
                file.unlink()


def remove_file_if_exists(path: Path):
    if path.is_file():
        path.unlink()


def tuple_if_none(value, size):
    if value is None:
        return (None,) * size
    else:
        return value
