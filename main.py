from fastapi import FastAPI
from router.ingredients import router

app = FastAPI()
app.include_router(router)