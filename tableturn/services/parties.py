
from tableturn.clock import get_clock
from uuid import uuid4

from sqlalchemy.orm import Session

from tableturn.errors import no_such_party, party_too_big
from tableturn.models import DiningTable, Party


def create_party(
    db: Session,
    name: str,
    covers: int,
    phone: str | None = None,
) -> Party:
    # Find the largest table in this branch.
    largest_table = (
        db.query(DiningTable.seats)
        .order_by(DiningTable.seats.desc())
        .first()
    )

    max_covers = largest_table[0] if largest_table else 0

    if covers > max_covers:
        raise party_too_big(max_covers=max_covers)

    # The database column is NOT NULL, so use a fallback
    # when the API request does not include a phone number.
    if phone is None:
        phone = "+10000000000"

    # Position is based only on parties currently waiting.
    waiting_count = (
        db.query(Party)
        .filter(Party.state == "waiting")
        .count()
    )

    party = Party(
        id=f"W{uuid4().hex[:12].upper()}",
        name=name.strip(),
        covers=covers,
        phone=phone,
        state="waiting",
        position=waiting_count + 1,
        joined_at=get_clock().replace(tzinfo=None),
    )

    db.add(party)
    db.commit()
    db.refresh(party)

    return party


def get_party(db: Session, party_id: str) -> Party:
    party = (
        db.query(Party)
        .filter(Party.id == party_id)
        .first()
    )

    if party is None:
        raise no_such_party(party_id)

    return party


def list_parties(db: Session) -> list[Party]:
    return (
        db.query(Party)
        .order_by(Party.position)
        .all()
    )
