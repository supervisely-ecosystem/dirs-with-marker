import os
import json

import supervisely as sly

DATA_DIR = "data"
ARCHIVE_PATH = os.path.join(DATA_DIR, "input_archive.zip")
EXCTRACT_PATH = os.path.join(DATA_DIR, "extracted")

# 1. Extracting the archive and removing junk files.
sly.fs.unpack_archive(ARCHIVE_PATH, EXCTRACT_PATH, remove_junk=True)

# 2. Specifying the marker we want to find.
MARKERS = "config.json"

# 3. Iterating over directories with markers without checking them.
for directory in sly.fs.dirs_with_marker(EXCTRACT_PATH, MARKERS, ignore_case=True):
    print(f"The directory with the marker '{MARKERS}' is found: '{directory}'")


# 4. Defining the check function.
def check_function(directory: str) -> bool:
    config = json.load(open(os.path.join(directory, MARKERS)))
    images_dir = os.path.join(directory, "images")
    anns_dir = os.path.join(directory, "anns")

    return config.get("valid") is True and os.path.isdir(images_dir) and os.path.isdir(anns_dir)


# 5. Iterating over directories with directories which contains markers and passed the check.
for checked_directory in sly.fs.dirs_with_marker(
    EXCTRACT_PATH, MARKERS, check_function=check_function, ignore_case=True
):
    print(f"The directory '{checked_directory}' is valid.")
