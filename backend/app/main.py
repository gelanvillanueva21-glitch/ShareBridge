from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import users

app = FastAPI(
    title="ShareBridge API",
    description="Local donation network connecting donors, volunteers, and charities.",
    version="1.0.0"
)

# ---------------------------------------------------------------------------
# CORS Middleware
# ---------------------------------------------------------------------------
# Allows our React frontend (localhost:5173) to communicate with this API.
# 'allow_credentials=True' is required for cookies (our HttpOnly refresh token).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,   # Must be True for HttpOnly cookies to work
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------
app.include_router(users.router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "ShareBridge API is running."}
