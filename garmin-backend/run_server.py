"""PyInstaller entry point: run the FastAPI app via uvicorn programmatically."""

import uvicorn

from main import app  # static import so PyInstaller captures the dependency graph

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
