from fastapi import FastAPI

from domain.download import download_router
from domain.upload import upload_router

app = FastAPI()


app.include_router(download_router.router)
app.include_router(upload_router.router)
