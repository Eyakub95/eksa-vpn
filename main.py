from datetime import datetime, timezone
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .config import settings
from .db import Base, engine, get_db
from .models import Account, Subscription, VpnServer
from .schemas import UserCreate, UserPatch, ServerCreate
from .security import verify_password, hash_password, create_token
from .deps import current_account, admin_account

Base.metadata.create_all(bind=engine)
app = FastAPI(title="EKSA VPN API", version="0.1.0")
app.add_middleware(CORSMiddleware, allow_origins=[x.strip() for x in settings.cors_origins.split(",")],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok", "service": "eksa-vpn-api"}

@app.post("/auth/token")
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    account = db.query(Account).filter(Account.email == form.username).first()
    if not account or not verify_password(form.password, account.password_hash) or not account.is_active:
        raise HTTPException(status_code=401, detail="Incorrect credentials")
    return {"access_token": create_token(account.email, account.role), "token_type": "bearer"}

@app.get("/me")
def me(account: Account = Depends(current_account), db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter_by(account_id=account.id).first()
    return {"id": account.id, "email": account.email, "role": account.role,
            "is_active": account.is_active,
            "expires_at": sub.expires_at if sub else None,
            "quota_bytes": sub.quota_bytes if sub else 0,
            "used_bytes": sub.used_bytes if sub else 0}

@app.get("/client/config")
def client_config(account: Account = Depends(current_account), db: Session = Depends(get_db)):
    sub = db.query(Subscription).filter_by(account_id=account.id).first()
    now = datetime.now(timezone.utc)
    if not sub or (sub.expires_at and sub.expires_at <= now):
        raise HTTPException(status_code=403, detail="Subscription expired or missing")
    if sub.quota_bytes and sub.used_bytes >= sub.quota_bytes:
        raise HTTPException(status_code=403, detail="Data quota exhausted")
    nodes = db.query(VpnServer).filter_by(is_active=True).all()
    return {"servers": [{"id": n.id, "name": n.name, "country": n.country,
             "region": n.region, "hostname": n.hostname, "port": n.port,
             "protocol": n.protocol} for n in nodes]}

@app.get("/admin/users")
def list_users(_: Account = Depends(admin_account), db: Session = Depends(get_db)):
    rows = db.query(Account).filter(Account.role == "user").all()
    result = []
    for u in rows:
        s = db.query(Subscription).filter_by(account_id=u.id).first()
        result.append({"id": u.id, "email": u.email, "role": u.role, "is_active": u.is_active,
                       "expires_at": s.expires_at if s else None,
                       "quota_bytes": s.quota_bytes if s else 0,
                       "used_bytes": s.used_bytes if s else 0})
    return result

@app.post("/admin/users", status_code=201)
def create_user(data: UserCreate, _: Account = Depends(admin_account), db: Session = Depends(get_db)):
    if db.query(Account).filter_by(email=data.email).first():
        raise HTTPException(status_code=409, detail="Email already exists")
    user = Account(email=data.email, password_hash=hash_password(data.password), role="user")
    db.add(user); db.flush()
    db.add(Subscription(account_id=user.id, expires_at=data.expires_at, quota_bytes=data.quota_bytes))
    db.commit()
    return {"id": user.id, "email": user.email, "created": True}

@app.patch("/admin/users/{user_id}")
def update_user(user_id: int, data: UserPatch, _: Account = Depends(admin_account), db: Session = Depends(get_db)):
    user = db.query(Account).filter_by(id=user_id, role="user").first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if data.is_active is not None:
        user.is_active = data.is_active
    sub = db.query(Subscription).filter_by(account_id=user.id).first()
    if not sub:
        sub = Subscription(account_id=user.id); db.add(sub)
    if data.expires_at is not None: sub.expires_at = data.expires_at
    if data.quota_bytes is not None: sub.quota_bytes = data.quota_bytes
    db.commit()
    return {"updated": True}

@app.get("/admin/servers")
def list_servers(_: Account = Depends(admin_account), db: Session = Depends(get_db)):
    return db.query(VpnServer).all()

@app.post("/admin/servers", status_code=201)
def add_server(data: ServerCreate, _: Account = Depends(admin_account), db: Session = Depends(get_db)):
    node = VpnServer(**data.model_dump())
    db.add(node); db.commit(); db.refresh(node)
    return {"id": node.id, "created": True}
