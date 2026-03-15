from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.service_record import ServiceRecord
from app.models.user import User
from app.models.vehicle import Vehicle
from app.schemas.service_record import (
    ServiceRecordCreate,
    ServiceRecordResponse,
    ServiceRecordUpdate,
)

router = APIRouter(prefix="/vehicles/{vehicle_id}/service-records", tags=["service-records"])


def get_owned_vehicle(vehicle_id: int, db: Session, current_user: User) -> Vehicle:
    vehicle = (
        db.query(Vehicle)
        .filter(Vehicle.id == vehicle_id, Vehicle.owner_id == current_user.id)
        .first()
    )

    if not vehicle:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="vehicle not found",
        )

    return vehicle


@router.post("/", response_model=ServiceRecordResponse, status_code=status.HTTP_201_CREATED)
def create_service_record(
    vehicle_id: int,
    record_data: ServiceRecordCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_vehicle(vehicle_id, db, current_user)

    new_record = ServiceRecord(
        vehicle_id=vehicle_id,
        title=record_data.title,
        description=record_data.description,
        service_date=record_data.service_date,
        odometer=record_data.odometer,
        cost=record_data.cost,
        provider=record_data.provider,
    )

    db.add(new_record)
    db.commit()
    db.refresh(new_record)

    return new_record


@router.get("/", response_model=list[ServiceRecordResponse])
def list_service_records(
    vehicle_id: int,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    provider: Optional[str] = Query(default=None),
    date_from: Optional[date] = Query(default=None),
    date_to: Optional[date] = Query(default=None),
    min_odometer: Optional[int] = Query(default=None, ge=0),
    max_odometer: Optional[int] = Query(default=None, ge=0),
    sort: str = Query(default="desc", pattern="^(asc|desc)$"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_vehicle(vehicle_id, db, current_user)

    query = db.query(ServiceRecord).filter(ServiceRecord.vehicle_id == vehicle_id)

    if provider:
        query = query.filter(ServiceRecord.provider.ilike(f"%{provider}%"))

    if date_from:
        query = query.filter(ServiceRecord.service_date >= date_from)

    if date_to:
        query = query.filter(ServiceRecord.service_date <= date_to)

    if min_odometer is not None:
        query = query.filter(ServiceRecord.odometer >= min_odometer)

    if max_odometer is not None:
        query = query.filter(ServiceRecord.odometer <= max_odometer)

    if sort == "asc":
        query = query.order_by(ServiceRecord.service_date.asc(), ServiceRecord.id.asc())
    else:
        query = query.order_by(ServiceRecord.service_date.desc(), ServiceRecord.id.desc())

    records = query.offset(offset).limit(limit).all()

    return records


@router.get("/{record_id}", response_model=ServiceRecordResponse)
def get_service_record(
    vehicle_id: int,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_vehicle(vehicle_id, db, current_user)

    record = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.id == record_id, ServiceRecord.vehicle_id == vehicle_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="service record not found",
        )

    return record


@router.put("/{record_id}", response_model=ServiceRecordResponse)
def update_service_record(
    vehicle_id: int,
    record_id: int,
    record_data: ServiceRecordUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_vehicle(vehicle_id, db, current_user)

    record = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.id == record_id, ServiceRecord.vehicle_id == vehicle_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="service record not found",
        )

    record.title = record_data.title
    record.description = record_data.description
    record.service_date = record_data.service_date
    record.odometer = record_data.odometer
    record.cost = record_data.cost
    record.provider = record_data.provider

    db.commit()
    db.refresh(record)

    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_record(
    vehicle_id: int,
    record_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    get_owned_vehicle(vehicle_id, db, current_user)

    record = (
        db.query(ServiceRecord)
        .filter(ServiceRecord.id == record_id, ServiceRecord.vehicle_id == vehicle_id)
        .first()
    )

    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="service record not found",
        )

    db.delete(record)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)