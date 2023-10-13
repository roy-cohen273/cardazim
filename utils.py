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