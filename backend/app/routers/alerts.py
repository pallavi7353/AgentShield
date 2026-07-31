"""
alerts.py (router)
---------------------
GET /alerts
PUT /alerts/{id}  (acknowledge/resolve)

Requires VIEW_DASHBOARD permission.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.alert import AlertOut, AlertUpdate
from app.models.alert import Alert
from app.auth.dependencies import require_permission

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
    dependencies=[Depends(require_permission("VIEW_DASHBOARD"))],
)


@router.get("", response_model=List[AlertOut])
def list_alerts(db: Session = Depends(get_db)):
    return db.query(Alert).order_by(Alert.timestamp.desc()).all()


@router.put("/{alert_id}", response_model=AlertOut)
def update_alert_status(alert_id: int, payload: AlertUpdate, db: Session = Depends(get_db)):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert not found.")
    alert.status = payload.status
    db.commit()
    db.refresh(alert)
    return alert
