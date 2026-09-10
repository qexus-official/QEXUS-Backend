import os
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_KEY = os.getenv("ADMIN_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./qexus.db")
QEXC_TO_BDT = float(os.getenv("QEXC_TO_BDT", "0.10"))
AD_REWARD_QEXC = int(os.getenv("AD_REWARD_QEXC", "3"))
DAILY_BONUS_QEXC = int(os.getenv("DAILY_BONUS_QEXC", "10"))
MIN_WITHDRAW_BDT = float(os.getenv("MIN_WITHDRAW_BDT", "100"))
