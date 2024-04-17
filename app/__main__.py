# Path: app/__main__.py
# Description: Main entry point for the application when running the application using `python -m app`.

from . import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)