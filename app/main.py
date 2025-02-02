from fastapi import FastAPI
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import os
from routers.LyricsRouter import router as lyricsRouter
from routers.SearchRouter import router as searchRouter
from database.manager import Base, engine


app = FastAPI()

Base.metadata.create_all(bind=engine)


# Config
app.timeout = 10  # Timeout in seconds

# Middleware for trusted hosts (optional)
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])

# Routes
app.include_router(lyricsRouter, prefix="/search-lyrics")
app.include_router(searchRouter, prefix="/search-songs")

if __name__ == "__main__":
    import uvicorn

    port = os.getenv("PORT", 3000)
    uvicorn.run(app, host="0.0.0.0", port=int(port))
