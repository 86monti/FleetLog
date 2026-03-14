from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class VehicleCreate(BaseModel):
    make: str
    model: str
    year: int = Field(ge=1886, le=2100)
    registration_plate: Optional[str] = None
    vin: Optional[str] = None
    current_odometer: int = Field(ge=0)


class VehicleUpdate(BaseModel):
    make: str
    model: str
    year: int = Field(ge=1886, le=2100)
    registration_plate: Optional[str] = None
    vin: Optional[str] = None
    current_odometer: int = Field(ge=0)


class VehicleResponse(BaseModel):
    id: int
    owner_id: int
    make: str
    model: str
    year: int
    registration_plate: Optional[str]
    vin: Optional[str]
    current_odometer: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)