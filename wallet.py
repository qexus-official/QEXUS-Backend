from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import telegram_user
from ..services import get_or_create_user, wallet_for
from ..models import Transaction
router = APIRouter()

@router.get("/wallet")
def wallet(tg=Depends(telegram_user), db: Session=Depends(get_db)):
    u=get_or_create_user(db,tg); w=wallet_for(db,u.id)
    return {"balance_qexc":w.balance,"locked_qexc":w.locked_balance,"total_earned":w.total_earned,"total_withdrawn":w.total_withdrawn}

@router.get("/transactions")
def transactions(tg=Depends(telegram_user), db: Session=Depends(get_db)):
    u=get_or_create_user(db,tg)
    rows=db.query(Transaction).filter_by(user_id=u.id).order_by(Transaction.id.desc()).limit(100).all()
    return [{"id":x.id,"type":x.type,"amount_qexc":x.amount_qexc,"description":x.description,"status":x.status,"created_at":x.created_at.isoformat()} for x in rows]
