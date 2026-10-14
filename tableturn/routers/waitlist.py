
from datetime import timezone

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from tableturn.db import get_db
from tableturn.schemas import PartyCreate, PartyResponse
from tableturn.services.parties import create_party

router = APIRouter(tags=["Waitlist"])


@router.post(
    "/waitlist",
    response_model=PartyResponse,
    status_code=status.HTTP_201_CREATED,
)
def join_waitlist(
    payload: PartyCreate,
    response: Response,
    db: Session = Depends(get_db),
):
    party = create_party(
        db=db,
        name=payload.name,
        covers=payload.covers,
        phone=payload.phone,
    )

    joined_at = party.joined_at

    if joined_at.tzinfo is None:
        joined_at = joined_at.replace(tzinfo=timezone.utc)

    joined_at_text = (
        joined_at.astimezone(timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )

    party_id = str(party.id)
    response.headers["Location"] = f"/parties/{party_id}"

    return {
        "party_id": party_id,
        "name": party.name,
        "covers": party.covers,
        "state": party.state,
        "position": party.position,
        "joined_at": joined_at_text,
    }
