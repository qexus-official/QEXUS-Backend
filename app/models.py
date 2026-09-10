from datetime import datetime, date
from sqlalchemy import String, Integer, Float, DateTime, Date, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(Integer, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255))
    first_name: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    last_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Wallet(Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    balance: Mapped[float] = mapped_column(Float, default=0)
    locked_balance: Mapped[float] = mapped_column(Float, default=0)
    total_earned: Mapped[float] = mapped_column(Float, default=0)
    total_withdrawn: Mapped[float] = mapped_column(Float, default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    type: Mapped[str] = mapped_column(String(50))
    amount_qexc: Mapped[float] = mapped_column(Float)
    description: Mapped[str] = mapped_column(String(255))
    status: Mapped[str] = mapped_column(String(30), default="COMPLETED")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class DailyBonus(Base):
    __tablename__ = "daily_bonuses"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    claimed_on: Mapped[date] = mapped_column(Date)
    reward_qexc: Mapped[int] = mapped_column(Integer)
    __table_args__ = (UniqueConstraint("user_id", "claimed_on", name="uq_daily_bonus"),)

class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(255))
    reward_qexc: Mapped[int] = mapped_column(Integer, default=0)
    active: Mapped[bool] = mapped_column(default=True)
    url: Mapped[str | None] = mapped_column(Text)

class TaskCompletion(Base):
    __tablename__ = "task_completions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    task_id: Mapped[int] = mapped_column(ForeignKey("tasks.id"))
    completed_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint("user_id", "task_id", name="uq_task_completion"),)

class Withdrawal(Base):
    __tablename__ = "withdrawals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    amount_qexc: Mapped[float] = mapped_column(Float)
    amount_bdt: Mapped[float] = mapped_column(Float)
    method: Mapped[str] = mapped_column(String(30))
    account_number: Mapped[str] = mapped_column(String(30))
    status: Mapped[str] = mapped_column(String(30), default="PENDING")
    cancel_reason: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    processed_at: Mapped[datetime | None] = mapped_column(DateTime)

class Referral(Base):
    __tablename__ = "referrals"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    referrer_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    referred_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
