from fastapi import FastAPI

app = FastAPI(
    title="SamvadAI",
    description="Enterprise Voice AI Agent Platform",
    version="0.1.0",
)


@app.get("/")
async def health():
    return {
        "status": "ok",
        "service": "SamvadAI",
    }