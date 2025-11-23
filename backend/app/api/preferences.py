from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..services import auth as auth_service
from ..models import models
from ..schemas import preferences as schemas
from datetime import datetime

router = APIRouter(prefix="/api", tags=["preferences"])


@router.get("/preferences", response_model=schemas.PreferenceOut)
def get_preferences(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    pref = db.query(models.UserPreference).filter_by(user_id=current_user.id).first()
    if not pref:
        pref = models.UserPreference(user_id=current_user.id)
        db.add(pref)
        db.commit()
        db.refresh(pref)
    return pref


@router.put("/preferences", response_model=schemas.PreferenceOut)
def update_preferences(payload: schemas.PreferenceUpdate, db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    pref = db.query(models.UserPreference).filter_by(user_id=current_user.id).first()
    if not pref:
        pref = models.UserPreference(user_id=current_user.id)
    for k, v in payload.model_dump().items():
        setattr(pref, k, v)
    db.add(pref)
    db.commit()
    db.refresh(pref)
    return pref


@router.get("/alerts", response_model=list[schemas.AlertOut])
def list_alerts(db: Session = Depends(get_db), current_user=Depends(auth_service.get_current_user)):
    alerts = db.query(models.Alert).filter_by(user_id=current_user.id).order_by(models.Alert.triggered_at.desc()).all()
    return alerts
