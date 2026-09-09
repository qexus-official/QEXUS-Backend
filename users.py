from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import telegram_user
from ..services import get_or_create_user, wallet_for
router = APIRouter()

@router.post("/auth")
def auth(tg=Depends(telegram_user), db: Session=Depends(get_db)):
    u = get_or_create_user(db, tg); w = wallet_for(db, u.id)
    return {"user":{"id":u.id,"telegram_id":u.telegram_id,"username":u.username,"first_name":u.first_name},
            "wallet":{"balance_qexc":w.balance,"locked_qexc":w.locked_balance,"total_earned":w.total_earned,"total_withdrawn":w.total_withdrawn}}
