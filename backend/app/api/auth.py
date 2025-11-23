from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import auth as auth_schemas
from ..services import auth as auth_service
from ..utils.security import create_access_token
from datetime import timedelta
from ..core.config import settings
from ..core.database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register", response_model=auth_schemas.UserOut)
def register(payload: auth_schemas.UserCreate, db: Session = Depends(get_db)):
    user = auth_service.create_user(db, payload.email, payload.password)
    return user


@router.post("/login", response_model=auth_schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_access_token({"sub": user.id}, timedelta(minutes=settings.access_token_expire_minutes))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=auth_schemas.UserOut)
def me(current_user=Depends(auth_service.get_current_user)):
    return current_user
