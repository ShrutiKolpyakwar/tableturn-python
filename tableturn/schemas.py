from enum import Enum

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
)


class SectionType(str, Enum):
    WINDOW = "Window"
    GARDEN = "Garden"
    INDOOR = "Indoor"


class TableState(str, Enum):
    FREE = "free"
    SEATED = "seated"
    UNCLEARED = "uncleared"


class TableResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    no: str
    seats: int
    section: SectionType
    state: TableState


class TablesListResponse(BaseModel):
    branch: str
    tables: list[TableResponse]
    free: int


class PartyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=60)
    covers: int = Field(ge=1, le=20)
    phone: str | None = Field(
        default=None,
        pattern=r"^\+[1-9]\d{1,14}$",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Name must not be empty")

        return value


class PartyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    party_id: str
    name: str
    covers: int
    state: str
    position: int
    joined_at: str