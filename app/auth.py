import hashlib, hmac, json
from urllib.parse import parse_qsl
from fastapi import HTTPException
from .config import BOT_TOKEN

def validate_telegram_init_data(init_data: str) -> dict:
    if not BOT_TOKEN:
        raise HTTPException(500, "BOT_TOKEN is not configured")
    pairs = dict(parse_qsl(init_data, keep_blank_values=True))
    received_hash = pairs.pop("hash", None)
    if not received_hash:
        raise HTTPException(401, "Missing Telegram hash")
    data_check_string = "\n".join(f"{k}={pairs[k]}" for k in sorted(pairs))
    secret_key = hmac.new(b"WebAppData", BOT_TOKEN.encode(), hashlib.sha256).digest()
    calculated = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()
    if not hmac.compare_digest(calculated, received_hash):
        raise HTTPException(401, "Invalid Telegram initData")
    raw = pairs.get("user")
    if not raw:
        raise HTTPException(401, "Telegram user data missing")
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise HTTPException(401, "Invalid Telegram user data")
