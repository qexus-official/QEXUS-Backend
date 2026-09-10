from fastapi import Header, HTTPException
from .auth import validate_telegram_init_data

def telegram_user(x_telegram_init_data: str = Header(default="")):
    if not x_telegram_init_data:
        raise HTTPException(401, "X-Telegram-Init-Data header required")
    return validate_telegram_init_data(x_telegram_init_data)

def require_admin(x_admin_key: str = Header(default="")):
    from .config import ADMIN_KEY
    if not ADMIN_KEY or x_admin_key != ADMIN_KEY:
        raise HTTPException(403, "Admin access denied")
    return True
