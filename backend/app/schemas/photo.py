from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.photo import PhotoPurpose

class PhotoBase(BaseModel):
    purpose: PhotoPurpose
    reference_id: Optional[int] = None

class PhotoCreate(PhotoBase):
    # When creating, the API handles the file upload and generates the file_path.
    # The frontend doesn't send the file_path in JSON, it sends form-data.
    pass

class PhotoRead(PhotoBase):
    id: int
    uploader_id: int
    file_path: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

