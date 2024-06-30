from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel
from pydantic import BaseModel
from datetime import datetime
from strenum import StrEnum


# Shared properties
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    items: list["Item"] = Relationship(back_populates="owner")


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Shared properties
class ItemBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str = Field(min_length=1, max_length=255)


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = Field(default=None, min_length=1, max_length=255)  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)

# https://prod-api.exgold.co.kr/api/v1/main/detail/domestic/price
# {
#     "success": true,
#     "message": null,
#     "data": {
#         "domesticLivePriceDtoList": [
#             {
#                 "type": "Pt",
#                 "domesticPrice": 44463,
#                 "domesticPriceDon": 166737,
#                 "fluctuation": -204
#             },
#             {
#                 "type": "Pd",
#                 "domesticPrice": 43507,
#                 "domesticPriceDon": 163152,
#                 "fluctuation": 606
#             },
#             {
#                 "type": "Au",
#                 "domesticPrice": 103554,
#                 "domesticPriceDon": 388328,
#                 "fluctuation": 158
#             },
#             {
#                 "type": "Ag",
#                 "domesticPrice": 1300.9,
#                 "domesticPriceDon": 4879,
#                 "fluctuation": -2.1
#             }
#         ],
#         "regdate": "2024-06-29T06:00:10"
#     }
# }
# Shared properties
class GoldType(StrEnum):
   Pt = "Pt"
   Pd = "Pd"
   Au = "Au"
   Ag = "Ag" 


class Price(SQLModel):
    type: GoldType
    domesticPrice: float
    domesticPriceDon: float
    fluctuation: float


class PriceList(SQLModel):
    domesticLivePriceDtoList : list[Price]


class PriceResponse(BaseModel):
    data: PriceList
    regdate: datetime
    success: bool
    message: str | None
    