from pathlib import Path


def check_directory(directory: Path) -> bool:
    """Check that the given directory is valid."""
    if not directory.exists():
        print(f"Directory does not exist: '{directory}'")
        return False
    if not directory.is_dir():
        print(f"Not a directory: '{directory}'")
        return False
    return True


def max_directory_id(directory: Path):
    """Returns the largest id in the given directory.
    Returns -1 if the directory is empty.
    """
    return max((int(path.name) for path in directory.iterdir() if path.name.isnumeric()), default=-1)
