from pydantic import BaseModel, Field


class UploadResponse(BaseModel):
    unique_id: str = Field(..., description="Uploaded file identifier")
