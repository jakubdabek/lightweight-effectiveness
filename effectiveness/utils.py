from pathlib import Path
import shutil

def clear_dir(path):
    path = Path(path)
    if path.exists():
        for file in path.iterdir():
            if file.is_dir():
                shutil.rmtree(file)
            else:
                file.unlink()


def tuple_if_none(value, size):
    if value is None:
        return (None,) * size
    else:
        return value
