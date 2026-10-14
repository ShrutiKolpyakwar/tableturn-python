"""Domain refusals and the error types. No FastAPI or Starlette import: services raise these, and
`handlers.py` turns them into application/problem+json.

The class attributes below are the single source of truth for status, type and title. Routes never build error
responses; services raise, the handler maps.
"""
from fastapi import HTTPException, status


class TableTurnError(HTTPException):
    def __init__(
        self,
        status_code: int,
        error_type: str,
        title: str,
        detail: str,
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "type": f"/errors/{error_type}",
                "title": title,
                "status": status_code,
                "detail": detail,
            },
        )


def no_such_branch(branch: str):
    return TableTurnError(
        status_code=status.HTTP_404_NOT_FOUND,
        error_type="no-such-branch",
        title="Branch not found",
        detail=f"Branch '{branch}' does not exist.",
    )


def no_such_table(table_no: str):
    return TableTurnError(
        status_code=status.HTTP_404_NOT_FOUND,
        error_type="no-such-table",
        title="Table not found",
        detail=f"Table '{table_no}' does not exist.",
    )

def party_too_big(max_covers: int):
    error = TableTurnError(
        status_code=status.HTTP_400_BAD_REQUEST,
        error_type="party-too-big",
        title="Party too big",
        detail=f"Maximum party size is {max_covers}.",
    )
    error.detail["max_covers"] = max_covers
    return error


def no_such_party(party_id: str):
    return TableTurnError(
        status_code=status.HTTP_404_NOT_FOUND,
        error_type="no-such-party",
        title="Party not found",
        detail=f"Party '{party_id}' does not exist.",
    )
  
