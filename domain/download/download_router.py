from fastapi import APIRouter

router = APIRouter(
    prefix="/download",
)


@router.get("/")
def downlaod_file():
    return "downloaded"
