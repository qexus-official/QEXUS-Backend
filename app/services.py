from datetime import datetime, date
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .models import User, Wallet, Transaction, DailyBonus, Task, TaskCompletion
from .config import DAILY_BONUS_QEXC, AD_REWARD_QEXC

def get_or_create_user(db: Session, tg: dict):
    telegram_id = int(tg["id"])
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user:
        user = User(telegram_id=telegram_id, username=tg.get("username"), first_name=tg.get("first_name"))
        db.add(user); db.flush(); db.add(Wallet(user_id=user.id))
    else:
        user.username = tg.get("username"); user.first_name = tg.get("first_name"); user.last_seen = datetime.utcnow()
    db.commit(); db.refresh(user)
    return user

def wallet_for(db: Session, user_id: int):
    wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    if not wallet:
        wallet = Wallet(user_id=user_id); db.add(wallet); db.commit(); db.refresh(wallet)
    return wallet

def add_reward(db: Session, user_id: int, amount: float, description: str, tx_type="EARN"):
    if amount <= 0: raise HTTPException(400, "Reward must be positive")
    w = wallet_for(db, user_id)
    w.balance += amount; w.total_earned += amount
    db.add(Transaction(user_id=user_id, type=tx_type, amount_qexc=amount, description=description))
    db.commit(); db.refresh(w); return w

def claim_daily_bonus(db: Session, user_id: int):
    today = date.today()
    if db.query(DailyBonus).filter_by(user_id=user_id, claimed_on=today).first():
        raise HTTPException(409, "Daily bonus already claimed today")
    db.add(DailyBonus(user_id=user_id, claimed_on=today, reward_qexc=DAILY_BONUS_QEXC))
    return add_reward(db, user_id, DAILY_BONUS_QEXC, "Daily bonus", "DAILY_BONUS")

def reward_ad(db: Session, user_id: int):
    return add_reward(db, user_id, AD_REWARD_QEXC, "Rewarded ad", "AD")

def complete_task(db: Session, user_id: int, task_id: int):
    task = db.query(Task).filter_by(id=task_id, active=True).first()
    if not task: raise HTTPException(404, "Task not found")
    if db.query(TaskCompletion).filter_by(user_id=user_id, task_id=task_id).first():
        raise HTTPException(409, "Task already completed")
    db.add(TaskCompletion(user_id=user_id, task_id=task_id))
    return add_reward(db, user_id, task.reward_qexc, task.title, "TASK")
