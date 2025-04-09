from fastapi import FastAPI
from app.api.routes import router
from app.database import init_db

app = FastAPI(title="Bank Account API", log_level="debug")

init_db()

app.include_router(router)

@app.get("/")
def redd_root():
    return {"message": "Welcome"}