from datetime import timezone
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from tableturn.db import get_db
from tableturn.schemas import PartyCreate, PartyResponse
from tableturn.services.parties import (
    create_party,
    get_party,
    list_parties,
)

router = APIRouter(
    prefix="/parties",
    tags=["Parties"],
)


@router.post(
    "",
    response_model=PartyResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_party(
    payload: PartyCreate,
    db: Session = Depends(get_db),
):
    return create_party(
        db=db,
        name=payload.name,
        covers=payload.covers,
        phone=payload.phone,
    )


@router.get(
    "",
    response_model=list[PartyResponse],
)
def read_parties(
    db: Session = Depends(get_db),
):
    return list_parties(db)



@router.get(
    "/{party_id}",
    response_model=PartyResponse,
)
def read_one_party(
    party_id: str,
    db: Session = Depends(get_db),
):
    party = get_party(db, party_id)

    joined_at = party.joined_at
    if joined_at.tzinfo is None:
        joined_at = joined_at.replace(
            tzinfo=timezone.utc
        )

    joined_at_text = (
        joined_at.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    return {
        "party_id": str(party.id),
        "name": party.name,
        "covers": party.covers,
        "state": party.state,
        "position": party.position,
        "joined_at": joined_at_text,
    }
