from pydantic import BaseModel

class UploadResponse(BaseModel):
    message: str
    filename: str
    original_name: str
    file_path: str
    file_type: str
    size_bytes: int
