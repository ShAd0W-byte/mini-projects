# Directory File Organiser

A Python-based file management utility that scans directories, organises files by type, generates reports, detects duplicate files, and provides an undo mechanism for organised files.

## Features

- Scan a directory and group files by extension
- Organise files into categories:
  - Images
  - Documents
  - Videos
  - Code
  - Others
- Generate a directory report containing:
  - Total number of files
  - Size of each category
  - Largest file
  - Newest file
  - Oldest file
- Detect duplicate files using:
  - File size comparison
  - SHA-256 content hashing
- Maintain a movement log for organised files
- Undo file organisation using the movement log

## Technologies

- Python
- os
- os.path
- shutil
- hashlib

## How It Works

### Scan

Scans the selected directory and groups files based on their extensions.

### Organise

Files are classified based on their extensions and moved into category directories.

### Generate Report

Creates a report containing file counts, category sizes, and file metadata such as the largest, newest, and oldest files.

### Find Duplicates

Files are first grouped based on file size. Files with matching sizes are then compared using SHA-256 hashes to identify files with identical content.

### Undo

The organisation process records file movements in a log. The undo operation reads the log and moves the files back to their original locations.

## Usage

Run the Python program:

```bash
python3 main.py
