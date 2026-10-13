from enum import Enum

from pydantic import BaseModel, ConfigDict


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