from typing import Optional

from app.models.core import CoreModel, IDModelMixin, MSIDMixin


class UserBase(CoreModel):
    id: Optional[str]
    username: Optional[str]
    date_of_birth: Optional[str]
    member_id: Optional[str]
    group_number: Optional[str]
    set_number: Optional[str]


class UserCreate(UserBase):
    pass


class UserUpdate(CoreModel):
    date_of_birth: Optional[str]
    member_id: Optional[str]
    group_number: Optional[str]
    set_number: Optional[str]


class UserInDB(IDModelMixin, UserBase):
    pass


class UserPublic(MSIDMixin, UserBase):
    pass
