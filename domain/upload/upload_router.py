from fastapi import APIRouter, Form, UploadFile
from domain.upload.upload_schema import UploadResponse
from domain.upload.upload_service import handle_upload

router = APIRouter(
    prefix="/upload",
)


@router.post("/file", response_model=UploadResponse)
async def upload_file(
    file: UploadFile,
    password: str = Form(...),
):
    unique_id = await handle_upload(file, password)

    return {"unique_id": unique_id}
