from __future__ import annotations

from datetime import datetime, timedelta
from typing import Union

import jwt

from config import settings


def generate_jwt(user_id: int, role_id: int) -> str:
    """
    Generate JWT token

    Args:
        user_id: ID of the user to include in the token

    Returns:
        JWT token as string
    """
    SECRET_KEY = settings.secret_key
    expiration = datetime.now() + timedelta(days=1)
    payload = {
        "user_id": user_id,
        "role_id": role_id,
        "exp": expiration,
        "iat": datetime.now(),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
