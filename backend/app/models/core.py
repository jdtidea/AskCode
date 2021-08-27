from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator


class CoreModel(BaseModel):
    # Any common logic to be shared by all models goes here

    pass


class DateTimeModelMixin(BaseModel):
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @validator("created_at", "updated_at", pre=True)
    def default_datetime(cls, value: datetime) -> datetime:
        return value or datetime.datetime.now()


class MSIDMixin(BaseModel):
    displayName: Optional[str]
    employeeId: Optional[str]
    given_name: Optional[str]
    locale: Optional[str]
    family_name: Optional[str]
    email: Optional[str]


class IDModelMixin(BaseModel):
    id: int