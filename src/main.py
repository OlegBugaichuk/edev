from fastapi import FastAPI

from core.auth.routers import router

app = FastAPI()

app.include_router(router)