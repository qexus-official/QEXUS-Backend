from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import Base, engine
from .routes import users, wallet, rewards, withdrawals, admin

Base.metadata.create_all(bind=engine)
app = FastAPI(title="QEXUS Backend API", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False,
                   allow_methods=["*"], allow_headers=["*"])
app.include_router(users.router, prefix="/api")
app.include_router(wallet.router, prefix="/api")
app.include_router(rewards.router, prefix="/api")
app.include_router(withdrawals.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

@app.get("/")
def root():
    return {"ok": True, "service": "QEXUS Backend", "version": "1.0.0"}

@app.get("/health")
def health():
    return {"ok": True}
