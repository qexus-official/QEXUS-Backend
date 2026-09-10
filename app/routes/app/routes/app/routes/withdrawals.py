import re
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import telegram_user
from ..schemas import WithdrawalCreate
from ..services import get_or_create_user, wallet_for
from ..models import Withdrawal, Transaction
from ..config import QEXC_TO_BDT, MIN_WITHDRAW_BDT
router=APIRouter()

@router.post("/withdrawals")
def create_withdrawal(p:WithdrawalCreate,tg=Depends(telegram_user),db:Session=Depends(get_db)):
    u=get_or_create_user(db,tg); method=p.method.strip(); number=p.account_number.strip().replace(" ","").replace("-","")
    if method not in {"bKash","Nagad"}: raise HTTPException(400,"Unsupported withdrawal method")
    if not re.fullmatch(r"01[3-9]\d{8}",number): raise HTTPException(400,"Invalid Bangladesh mobile number")
    if p.amount_bdt < MIN_WITHDRAW_BDT: raise HTTPException(400,f"Minimum withdrawal is {MIN_WITHDRAW_BDT:g} BDT")
    amount_qexc=round(p.amount_bdt/QEXC_TO_BDT,2); w=wallet_for(db,u.id)
    if w.balance < amount_qexc: raise HTTPException(400,"Insufficient balance")
    w.balance-=amount_qexc; w.locked_balance+=amount_qexc
    db.add(Transaction(user_id=u.id,type="WITHDRAWAL_LOCK",amount_qexc=-amount_qexc,description=f"{method} withdrawal requested",status="PENDING"))
    wd=Withdrawal(user_id=u.id,amount_qexc=amount_qexc,amount_bdt=p.amount_bdt,method=method,account_number=number)
    db.add(wd); db.commit(); db.refresh(wd)
    return {"ok":True,"withdrawal_id":wd.id,"status":wd.status}
