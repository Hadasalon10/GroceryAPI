"""Entry point for running the app, e.g. `uvicorn main:app --reload`.
Actual app construction lives in app/main.py.
"""

from app.main import app

__all__ = ["app"]
