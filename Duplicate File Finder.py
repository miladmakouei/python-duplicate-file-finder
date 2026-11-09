
import hashlib
from pathlib import Path


def calculate_file_hash(file_path):
    hasher = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(4096), b""):
            hasher.update(chunk)

    return hasher.hexdigest()


def find_duplicate_files(directory):
    file_hashes = {}
    scanned_files = 0
    unreadable_files = 0

    for file_path in directory.rglob("*"):
        if not file_path.is_file():
            continue

        try:
            file_hash = calculate_file_hash(file_path)

            file_hashes.setdefault(file_hash, []).append(file_path)
            scanned_files += 1

        except OSError:
            unreadable_files += 1
            print(f"Could not read: {file_path}")

    duplicates = [
        paths
        for paths in file_hashes.values()
        if len(paths) > 1
    ]

    return duplicates, scanned_files, unreadable_files


def display_report(duplicates, scanned_files, unreadable_files):

    print("\nDUPLICATE FILE FINDER REPORT")
    print("=" * 50)

    print(f"Scanned Files: {scanned_files}")
    print(f"Unreadable Files: {unreadable_files}")
    print(f"Duplicate Groups: {len(duplicates)}")

    if not duplicates:
        print("\nNo duplicate files found.")
        return

    print("\nDuplicate Files")
    print("-" * 50)

    for group_number, group in enumerate(duplicates, start=1):
        print(f"\nGroup {group_number}:")

        for file_path in group:
            print(f"- {file_path}")


def main():
    print("Duplicate File Finder")
    print("-" * 30)

    folder_path = input("Enter folder path: ").strip()

    if not folder_path:
        print("Folder path cannot be empty.")
        return

    directory = Path(folder_path).expanduser()

    if not directory.exists():
        print("The specified path does not exist.")
        return

    if not directory.is_dir():
        print("The specified path is not a directory.")
        return

    duplicates, scanned_files, unreadable_files = (
        find_duplicate_files(directory)
    )

    display_report(
        duplicates,
        scanned_files,
        unreadable_files
    )


if __name__ == "__main__":
    main()
