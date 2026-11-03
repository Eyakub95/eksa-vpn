import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from .db import get_db
from .models import Account

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/token")

def current_account(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        email = payload.get("sub")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    account = db.query(Account).filter(Account.email == email, Account.is_active.is_(True)).first()
    if not account:
        raise HTTPException(status_code=401, detail="Account unavailable")
    return account

def admin_account(account: Account = Depends(current_account)):
    if account.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access required")
    return account
