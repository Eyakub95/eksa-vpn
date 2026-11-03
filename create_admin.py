from .db import Base, engine, SessionLocal
from .models import Account
from .config import settings
from .security import hash_password

Base.metadata.create_all(bind=engine)
db = SessionLocal()
try:
    existing = db.query(Account).filter_by(email=settings.admin_email).first()
    if existing:
        print("Admin already exists; no changes made.")
    else:
        db.add(Account(email=settings.admin_email, password_hash=hash_password(settings.admin_password), role="admin"))
        db.commit()
        print(f"Created admin: {settings.admin_email}")
finally:
    db.close()
