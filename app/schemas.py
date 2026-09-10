from pydantic import BaseModel, Field

class WithdrawalCreate(BaseModel):
    amount_bdt: float = Field(gt=0)
    method: str
    account_number: str

class AdminWithdrawalAction(BaseModel):
    action: str
    reason: str | None = None

class TaskCreate(BaseModel):
    title: str
    reward_qexc: int = Field(ge=0)
    url: str | None = None
