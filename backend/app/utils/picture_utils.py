# backend/app/utils/picture_utils.py
"""Utility helpers for saving uploaded picture files.

The project stores all uploaded images under a top‑level ``Data`` directory with three
sub‑folders:

* ``posted_pictures`` – pictures that are *posted* by a user.
* ``sent_pictures``   – pictures that are *sent* to another user.
* ``profile_pictures`` – pictures that represent a user's profile image.

The :func:`save_picture` coroutine writes an ``UploadFile`` to the appropriate
sub‑folder, generates a unique filename, and returns a URL string that can be
stored in the database.  No database operation is performed here – the repository
layer creates the ORM record using the returned URL.
"""

import uuid
from pathlib import Path
from typing import Literal

import aiofiles
from fastapi import UploadFile

# Base directory is two levels up from this file (project root) → ``backend/app`` → ``..`` → ``..``
BASE_DIR = Path(__file__).resolve().parents[2] / "Data"
POSTED_DIR = BASE_DIR / "posted_pictures"
SENT_DIR = BASE_DIR / "sent_pictures"
PROFILE_DIR = BASE_DIR / "profile_pictures"

# Ensure the directories exist at import time.
for _dir in (POSTED_DIR, SENT_DIR, PROFILE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)


async def save_picture(file: UploadFile, folder: Literal["posted_pictures", "sent_pictures", "profile_pictures"]) -> str:
    """Save an uploaded image file to *folder* under the ``Data`` directory.

    Args:
        file: The FastAPI ``UploadFile`` received from the request.
        folder: One of ``"posted_pictures"``, ``"sent_pictures"`` or ``"profile_pictures"``.

    Returns:
        A URL string (relative to the project) that can be stored in the DB, e.g.
        ``"/data/profile_pictures/abcd1234.png"``.
    """
    # Resolve the target directory based on the requested folder name.
    target_dir = BASE_DIR / folder
    # Generate a unique filename to avoid collisions.
    suffix = Path(file.filename).suffix or ""
    unique_name = f"{uuid.uuid4().hex}{suffix}"
    target_path = target_dir / unique_name

    # Write the file content asynchronously.
    async with aiofiles.open(target_path, "wb") as out_file:
        content = await file.read()
        await out_file.write(content)

    # Return only the generated filename with its extension.
    return unique_name
