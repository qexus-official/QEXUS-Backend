from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import telegram_user
from ..services import get_or_create_user, claim_daily_bonus, reward_ad, complete_task
from ..models import Task
router=APIRouter()

@router.get("/tasks")
def tasks(db:Session=Depends(get_db)):
    return [{"id":x.id,"title":x.title,"reward_qexc":x.reward_qexc,"url":x.url} for x in db.query(Task).filter_by(active=True).all()]

@router.post("/rewards/daily")
def daily(tg=Depends(telegram_user), db:Session=Depends(get_db)):
    u=get_or_create_user(db,tg); w=claim_daily_bonus(db,u.id); return {"ok":True,"balance_qexc":w.balance}

@router.post("/rewards/ad")
def ad(tg=Depends(telegram_user), db:Session=Depends(get_db)):
    u=get_or_create_user(db,tg); w=reward_ad(db,u.id); return {"ok":True,"balance_qexc":w.balance}

@router.post("/tasks/{task_id}/complete")
def task(task_id:int,tg=Depends(telegram_user),db:Session=Depends(get_db)):
    u=get_or_create_user(db,tg); w=complete_task(db,u.id,task_id); return {"ok":True,"balance_qexc":w.balance}
