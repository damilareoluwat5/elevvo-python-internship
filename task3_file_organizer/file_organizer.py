import logging
import shutil
import sys
from pathlib import Path

logging.basicConfig(
    filename="file_organizer.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

CATEGORIES = {
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Code": [".py", ".js", ".html", ".css", ".json", ".sql"],
    "Archives": [".zip", ".tar", ".gz", ".rar"]
}


def get_safe_destination(dest_path: Path) -> Path:
    """Prevents overwriting by renaming incoming duplicate files (e.g., file_1.txt)."""
    if not dest_path.exists():
        return dest_path
    counter = 1
    while True:
        candidate = dest_path.parent / f"{dest_path.stem}_{counter}{dest_path.suffix}"
        if not candidate.exists():
            return candidate
        counter += 1


def get_category(extension: str) -> str:
    """Maps a file extension to its destination subfolder."""
    ext = extension.lower()
    for folder, extensions in CATEGORIES.items():
        if ext in extensions:
            return folder
    return "Others"


def organize_directory(target_dir: str, dry_run: bool = False) -> None:
    """Scans a directory and moves files into subfolders by extension safely."""
    base = Path(target_dir).resolve()
    if not base.exists() or not base.is_dir():
        print(f"Error: '{target_dir}' is not a valid directory.")
        return

    files = [
        f for f in base.iterdir()
        if f.is_file() and not f.name.startswith(".") and f.name != Path(__file__).name
    ]

    if not files:
        print("Directory is empty or contains no movable files.")
        return

    for file_path in files:
        category = get_category(file_path.suffix)
        dest_folder = base / category
        safe_dest = get_safe_destination(dest_folder / file_path.name)

        summary = f"File: {file_path.name} | Source: {base.name}/ -> Destination: {category}/{safe_dest.name}"
        print(f"{'[DRY-RUN] ' if dry_run else ''}{summary}")
        logging.info(summary)

        if not dry_run:
            try:
                dest_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(file_path), str(safe_dest))
            except PermissionError:
                print(f"Permission denied: {file_path.name}")
                logging.error(f"Permission denied: {file_path.name}")


if __name__ == "__main__":
    folder_arg = sys.argv[1] if len(sys.argv) > 1 else "."
    is_dry_run = "--dry-run" in sys.argv
    organize_directory(folder_arg, dry_run=is_dry_run)
