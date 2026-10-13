
from sqlalchemy.orm import Session

from tableturn.errors import no_such_table
from tableturn.models import DiningTable, Seating


def get_table_state(db: Session, table_no: str) -> str:
    seating = (
        db.query(Seating)
        .filter(
            Seating.table_no == table_no,
            Seating.status.in_(["seated", "uncleared"]),
        )
        .order_by(Seating.id.desc())
        .first()
    )

    if seating is None:
        return "free"

    return seating.status


def list_tables(
    db: Session,
    branch: str = "Baner",
    section: str | None = None,
    state: str | None = None,
):
    query = db.query(DiningTable)

    if section is not None:
        query = query.filter(DiningTable.section == section)

    tables = query.order_by(DiningTable.no).all()
    results = []

    for table in tables:
        current_state = get_table_state(db, table.no)

        if state is not None and current_state != state:
            continue

        results.append(
            {
                "no": table.no,
                "seats": table.seats,
                "section": table.section,
                "state": current_state,
            }
        )

    return {
        "branch": branch,
        "tables": results,
        "free": sum(
            1 for table in results if table["state"] == "free"
        ),
    }


def get_table(db: Session, table_no: str):
    table = (
        db.query(DiningTable)
        .filter(DiningTable.no == table_no)
        .first()
    )

    if table is None:
        raise no_such_table(table_no)

    return {
        "no": table.no,
        "seats": table.seats,
        "section": table.section,
        "state": get_table_state(db, table.no),
    }