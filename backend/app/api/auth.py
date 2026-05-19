from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel, EmailStr
from app.db import get_db
from app.models import User
from app.security import hash_password, verify_password, create_access_token

router = APIRouter()


class Creds(BaseModel):
    email: EmailStr
    password: str


@router.post("/register")
async def register(c: Creds, db: AsyncSession = Depends(get_db)):
    exists = (await db.execute(select(User).where(User.email == c.email))).scalar_one_or_none()
    if exists: raise HTTPException(400, "Email already registered")
    u = User(email=c.email, hashed_password=hash_password(c.password))
    db.add(u); await db.commit()
    return {"access_token": create_access_token(c.email), "token_type": "bearer"}


@router.post("/login")
async def login(c: Creds, db: AsyncSession = Depends(get_db)):
    u = (await db.execute(select(User).where(User.email == c.email))).scalar_one_or_none()
    if not u or not verify_password(c.password, u.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": create_access_token(c.email), "token_type": "bearer"}
