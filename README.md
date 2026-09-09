# QEXUS Backend

FastAPI backend for the QEXUS Telegram Mini App.

Includes Telegram initData validation, users, wallet, transactions, daily bonus,
test ad rewards, tasks, bKash/Nagad withdrawal requests, locked balance, and admin
approve/cancel with automatic refund.

Install:
`pip install -r requirements.txt`

Configure `.env` from `.env.example`. Never put BOT_TOKEN in frontend code.

Run:
`uvicorn app.main:app --host 0.0.0.0 --port 8000`

The frontend should send the raw Telegram Mini App initData in:
`X-Telegram-Init-Data`

The rewarded-ad endpoint is TEST ONLY. Connect a real ad provider with
server-side verification before enabling real rewards.

Production: use PostgreSQL + HTTPS and restrict CORS to the exact Mini App origin.
