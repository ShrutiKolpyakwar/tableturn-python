import csv
from pathlib import Path

from sqlalchemy.orm import Session

from tableturn import db as database
from tableturn.models import DiningTable, Seating
from tableturn.settings import Settings


def get_seed_csv_path() -> Path:
    settings = Settings()
    seed_dir = Path(settings.seed_dir)

    if not seed_dir.is_absolute():
        seed_dir = Path.cwd() / seed_dir

    csv_path = seed_dir / "tables.csv"

    if not csv_path.exists():
        fallback = (
            Path(__file__).resolve().parents[2]
            / "seed"
            / "tables.csv"
        )
        if fallback.exists():
            csv_path = fallback

    if not csv_path.exists():
        raise FileNotFoundError(
            f"Seed CSV not found: {csv_path}"
        )

    return csv_path


def seed_tables(session: Session) -> None:
    if session.query(DiningTable).count() > 0:
        return

    csv_path = get_seed_csv_path()

    with csv_path.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as file:
        reader = csv.DictReader(file)

        for row in reader:
            table_no = (
                row.get("no")
                or row.get("table_no")
                or row.get("number")
                or row.get("id")
            )

            seats = row.get("seats")
            section = row.get("section")

            if not table_no or not seats or not section:
                raise ValueError(f"Invalid CSV row: {row}")

            session.add(
                DiningTable(
                    no=table_no.strip(),
                    seats=int(seats),
                    section=section.strip(),
                )
            )

        session.commit()


def initialize_database() -> None:
    database.configure_database()

    # The model imports above register both tables with Base.metadata.
    database.Base.metadata.create_all(bind=database.engine)

    session = database.SessionLocal()
    try:
        seed_tables(session)
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
