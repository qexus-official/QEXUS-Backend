from app.database import Base, engine, SessionLocal
from app.models import Task
Base.metadata.create_all(bind=engine)
db=SessionLocal()
if db.query(Task).count()==0:
    db.add_all([Task(title="Visit QEXUS community",reward_qexc=5,url="https://t.me/"),
                Task(title="Complete starter task",reward_qexc=10)])
    db.commit()
print("QEXUS database ready.")
