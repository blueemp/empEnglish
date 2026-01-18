"""API routers package."""

from . import health
from . import auth
from . import users
from . import questions
from . import practice

__all__ = ["health", "auth", "users", "questions", "practice"]
