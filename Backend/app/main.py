from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.payments import router as payment_router
# from app.webhook import router as webhook_router

app = FastAPI()

# CORS FIX (IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(payment_router)
# app.include_router(webhook_router)

@app.get("/")
def home():
    return {"message": "Server running"}