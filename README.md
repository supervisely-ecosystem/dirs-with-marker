---
description: >-
A tutorial on how to find directories with specific markers (filename) and check them for some conditions using `sly.fs.dirs_with_marker()` function.
---

# Finding directories with specific markers

## Introduction

First of all, let's talk about the use cases of this function. When working with import apps, there are often cases where we need a specific structure for input data to ensure the application functions correctly. Frequently, it's necessary to identify a specific file marker that serves as a reference point for determining the rest of the structure. However, user-provided data can have varying structures. For instance, the target directory might not be in the root directory but nested within several other directories, or the data may contain not just one but multiple suitable directories. <br>
For example, we're trying to find a directory with a `config.json` file in it. The directory structure might look like this:

```text
📂 input_dir
┣ 📂 nested_dir_1
┃ ┣ 📂 nested_dir_2
┃ ┃ ┗ 📂 nested_dir_3
┃ ┃   ┣ 📄 config.json
┃ ┃   ┗ 📄 data.csv
┗ 📂 nested_dir_4
  ┣ 📄 config.json
  ┗ 📄 data.csv
```

So, in this case, we need to find two directories: `nested_dir_3` and `nested_dir_4`. It's not a problem to find them, but why implement the same logic every time? It's much easier to use a function that will do it for us everywhere we need it. <br>
And it's just a part of the problem, we're trying to solve here. Same as finding directories, we usually need to check them for some conditions. Because the file we've found maybe incorrect and a user may just forget to delete it, or the directory may not contain other needed files. If we try to work with the data from this directory, we may have an error or, much worse, incorrect results. Of course, we can write the function that will check the directory for us, and pass the directories to it one by one. Well, while using `sly.fs.dirs_with_marker()` we still need to have this function, if we need to check the directory for some conditions, but we can make this process more convenient and the code more readable and clear. <br>

## Function signature

```python
sly.fs.dirs_with_marker(
    input_path: str,
    markers: Union[str, List[str]],
    check_function: Optional[Callable] = None,
    ignore_case: Optional[bool] = False,
) -> Generator[str, None, None]:
```

## Parameters

|    Parameters    |          Type           |                              Description                               |
| :--------------: | :---------------------: | :--------------------------------------------------------------------: |
|   `input_path`   |          `str`          |     Path to the directory from which the search will be performed.     |
|    `markers`     | `Union[str, List[str]]` |         Filename or list of filenames, which will be searched.         |
| `check_function` |  `Optional[Callable]`   | Function that will be used to check the directory for some conditions. |
|  `ignore_case`   |    `Optional[bool]`     |  If `True`, the search will be case-insensitive. Default is `False`.   |

## Data Example

We prepared a short Python script, that will unpack an archive (as an example of input data from a user) and find directories with `config.json` files in them. Then it will check if they're valid. Conditions for checking are the following:

- The directory must contain `config.json` file.
- The `config.json` file must have a key `valid`, and its value must be `true`.
- The directory must contain two other subdirectories: `images` and `anns`.

!!!! ADD TREE WITH ARCHIVE !!!

You can find the above demo archive in the data directory of the dirs-with-marker repo - [here](https://github.com/supervisely-ecosystem/dirs-with-marker/blob/master/data)

## Tutorial content

- [Step 1. How to extract the archive and clean it of junk files](#step-1-how-to-extract-the-archive-and-clean-it-of-junk-files)
- [Step 2. How to find directories with markers](#step-2-how-to-find-directories-with-markers)
- [Step 3. How to check directories for some conditions](#step-3-how-to-check-directories-for-some-conditions)
- [Example of the final code](#example-of-the-final-code)

Everything you need to reproduce [this tutorial is on GitHub](https://github.com/supervisely-ecosystem/dirs-with-marker): [main.py](https://github.com/supervisely-ecosystem/dirs-with-marker/blob/master/src/main.py).

## Step 1. How to extract the archive and clean it of junk files

It's not a rare case, when the archive from a user contains some unnecessary files. For example, the archive may contain a `__MACOSX` directory or `.DS_Store` files, which are created by macOS. If we don't handle them, we may have an error while working with the data, so in most cases, it's much easier to delete them. <br>

To extract the archive, we'll use the `sly.fs.unpack_archive()` function:

```python
import os
import json
import supervisely as sly

DATA_DIR = "data"
ARCHIVE_PATH = os.path.join(DATA_DIR, "input_archive.zip")
EXCTRACT_PATH = os.path.join(DATA_DIR, "extracted")

sly.fs.unpack_archive(ARCHIVE_PATH, EXCTRACT_PATH, remove_junk=True)

```

ℹ️ If the archive was already extracted and you want to remove junk files from it, you can use the `sly.fs.remove_junk_from_dir()` function:

```python
sly.fs.remove_junk_from_dir(EXCTRACT_PATH)
```

Now we have a directory without junk files, and we can start searching for directories with markers.

## Step 2. How to find directories with markers

As we already have a directory without junk files, we need to specify the markers we want to find. In our case, it's `config.json` file. We can pass it as a string or as a list of strings if we need to find multiple markers. <br><br>
ℹ️ If you're passing a list of markers it's important to mention, that they will be searched with the `OR`, not `AND` condition. It means that if you pass a list of markers, the function will return all directories that contain at least one of the markers. If you need a condition when the directory contains several specific markers, you can implement this check in the `check_function` parameter, we will talk about it in next section. <br><br>
Now we can use the `sly.fs.dirs_with_marker()` function to iterate over all directories with markers:

```python
MARKERS = "config.json"

for directory in sly.fs.dirs_with_marker(EXCTRACT_PATH, MARKERS, ignore_case=True):
    print(f"The directory with the marker '{MARKERS}' is found: '{directory}'")
```

Ok, we've found the directories, but how can we check them for some conditions? Let's talk about it in the next section.

## Step 3. How to check directories for some conditions

As we've already mentioned, we can pass a function to the `check_function` parameter, which will be used to check the directory for some conditions. This function must return `True` if the directory is valid and `False` otherwise. So, our conditions for checking were: `config.json` file must have a key `valid`, and its value must be `true`, and the directory must contain two other subdirectories: `images` and `anns`. Let's implement this check:

```python

```
