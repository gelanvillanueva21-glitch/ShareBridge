# backend/app/utils/image_helper.py
"""Utility for saving uploaded image files.

The function validates that the uploaded file is an image (jpeg, jpg, png, gif).
If the validation fails, it raises :class:`InvalidImageError`.
A random UUID based filename is generated, the file is stored under the
``data`` directory inside the application root and the appropriate sub‑folder
based on the supplied *role*.

Returned value: the generated filename (including extension) – e.g.
``"a3f4c9e2b1d34f2a8c9e7d5b6c1a2f3c.png"``.
"""

import uuid
import aiofiles


from pathlib import Path
from fastapi import UploadFile
from app.models.photo import PhotoPurpose
from app.exceptions import InvalidImageError

# Base directory: ``backend/app/data``
BASE_DIR = Path(__file__).resolve().parents[2] / "data"
# Ensure the three role‑specific folders exist
PFP_DIR = BASE_DIR / "Pfp"
MESSAGE_IMAGE_DIR = BASE_DIR / "MessageImage"
POSTED_IMAGE_DIR = BASE_DIR / "PostedImage"
PROOF_IMAGE_DIR = BASE_DIR / "ProofImage"
for _dir in (PFP_DIR, MESSAGE_IMAGE_DIR, POSTED_IMAGE_DIR, PROOF_IMAGE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)

# Allowed extensions (lower‑case) for image files
ALLOWED_EXTENSIONS = {".jpeg", ".jpg", ".png", ".gif"}


def _validate_image(file: UploadFile) -> str:
    """
    A helper function to validate the uploaded image file.
    """
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise InvalidImageError(
            f"Unsupported file type: {ext}. Allowed types are: {', '.join(ALLOWED_EXTENSIONS)}"
        )
    return ext


async def save_image(
    role: PhotoPurpose,
    file: UploadFile,
) -> str:
    
    """
    This function save the image to the data directory
    with three different directory depending on the role.
    It will check if the extension file is valid if not then
    it will raise an InvalidImageError.

    It also generate a unique filename for each saved image.
    """

    ext = _validate_image(file)
    target_dir = {
        PhotoPurpose.PROFILE: PFP_DIR,
        PhotoPurpose.PRIVATE_MESSAGE: MESSAGE_IMAGE_DIR,
        PhotoPurpose.DONATION_POST: POSTED_IMAGE_DIR,
        PhotoPurpose.DELIVERY_PROOF: PROOF_IMAGE_DIR,
    }[role]

    content = await file.read()
    while True:
        unique_name = f"{uuid.uuid4().hex}{ext}"
        target_path = target_dir / unique_name
        try:
            async with aiofiles.open(target_path, "xb") as out_file:
                await out_file.write(content)
            break
        except FileExistsError:
            continue
    return unique_name
