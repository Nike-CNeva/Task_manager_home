from pydantic import BaseModel

class UploadedFileResponse(BaseModel):
    filename: str
    bid_id: int
    file_type: str
    file_path: str
