from fastapi import FastAPI
from app.routes import brand

app = FastAPI(title="SentinelAI Digital Risk Intelligence")

app.include_router(brand.router)

@app.get("/")
def root():
    return {"status": "API running"}