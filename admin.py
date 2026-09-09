from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..deps import require_admin
from ..schemas import AdminWithdrawalAction, TaskCreate
from ..models import Withdrawal, Wallet, Transaction, Task
router=APIRouter()

@router.get("/admin/withdrawals")
def list_withdrawals(_=Depends(require_admin),db:Session=Depends(get_db)):
    rows=db.query(Withdrawal).order_by(Withdrawal.id.desc()).limit(200).all()
    return [{"id":x.id,"user_id":x.user_id,"amount_qexc":x.amount_qexc,"amount_bdt":x.amount_bdt,"method":x.method,"account_number":x.account_number,"status":x.status,"cancel_reason":x.cancel_reason,"created_at":x.created_at.isoformat()} for x in rows]

@router.post("/admin/withdrawals/{withdrawal_id}/action")
def action(withdrawal_id:int,p:AdminWithdrawalAction,_=Depends(require_admin),db:Session=Depends(get_db)):
    wd=db.query(Withdrawal).filter_by(id=withdrawal_id).first()
    if not wd: raise HTTPException(404,"Withdrawal not found")
    if wd.status!="PENDING": raise HTTPException(409,"Withdrawal already processed")
    w=db.query(Wallet).filter_by(user_id=wd.user_id).first()
    if p.action.upper()=="APPROVE":
        wd.status="PAID"; w.locked_balance-=wd.amount_qexc; w.total_withdrawn+=wd.amount_qexc
        db.add(Transaction(user_id=wd.user_id,type="WITHDRAWAL",amount_qexc=-wd.amount_qexc,description=f"{wd.method} withdrawal paid",status="PAID"))
    elif p.action.upper()=="CANCEL":
        wd.status="CANCELLED"; wd.cancel_reason=p.reason or "Cancelled by admin"; w.locked_balance-=wd.amount_qexc; w.balance+=wd.amount_qexc
        db.add(Transaction(user_id=wd.user_id,type="REFUND",amount_qexc=wd.amount_qexc,description="Withdrawal refunded",status="REFUNDED"))
    else: raise HTTPException(400,"Action must be APPROVE or CANCEL")
    wd.processed_at=datetime.utcnow(); db.commit()
    return {"ok":True,"status":wd.status}

@router.post("/admin/tasks")
def create_task(p:TaskCreate,_=Depends(require_admin),db:Session=Depends(get_db)):
    t=Task(title=p.title,reward_qexc=p.reward_qexc,url=p.url); db.add(t); db.commit(); db.refresh(t)
    return {"id":t.id,"title":t.title,"reward_qexc":t.reward_qexc,"url":t.url}
