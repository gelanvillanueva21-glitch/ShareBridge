from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.users import router as user_router
from app.routers.profile import router as profile_router
from app.routers.messages import router as message_router
from app.routers.claims import router as claim_router


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

# Routers connect to the main API
app.include_router(user_router, prefix="/api")
app.include_router(profile_router, prefix="/api")
app.include_router(message_router, prefix="/api")
app.include_router(claim_router, prefix="/api")



from fastapi.staticfiles import StaticFiles
from pathlib import Path

# Base data directory (absolute path)
BASE_DATA_DIR = Path(__file__).resolve().parents[2] / "Data"

# Ensure subfolders exist
for sub in ("profile_pictures", "sent_pictures", "posted_pictures"):
    (BASE_DATA_DIR / sub).mkdir(parents=True, exist_ok=True)

# Serve static files
app.mount("/avatars", StaticFiles(directory=str(BASE_DATA_DIR / "profile_pictures")), name="avatars")
app.mount("/sent", StaticFiles(directory=str(BASE_DATA_DIR / "sent_pictures")), name="sent")
app.mount("/posted", StaticFiles(directory=str(BASE_DATA_DIR / "posted_pictures")), name="posted")



@app.get("/")
async def root():
    return {"message": "ShareBridge API is running."}
