from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from tableturn.db import get_db
from tableturn.errors import no_such_branch
from tableturn.models import DiningTable
from tableturn.schemas import (
    SectionType,
    TableResponse,
    TableState,
    TablesListResponse,
)
from tableturn.services.tables import get_table, list_tables

router = APIRouter(tags=["Tables"])

# Baner is the branch currently configured for this project.
KNOWN_BRANCHES = {"Baner"}


def validate_branch(branch: str) -> None:
    if branch not in KNOWN_BRANCHES:
        raise no_such_branch(branch)


@router.get(
    "/branches/{branch}/tables",
    response_model=TablesListResponse,
)
def read_tables(
    branch: str,
    section: SectionType | None = Query(default=None),
    state: TableState | None = Query(default=None),
    db: Session = Depends(get_db),
):
    validate_branch(branch)

    return list_tables(
        db=db,
        section=section.value if section else None,
        state=state.value if state else None,
    )


@router.get(
    "/branches/{branch}/tables/{no}",
    response_model=TableResponse,
)
def read_table(
    branch: str,
    no: str,
    db: Session = Depends(get_db),
):
    validate_branch(branch)

    return get_table(db, no)