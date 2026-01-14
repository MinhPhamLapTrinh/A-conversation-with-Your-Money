from fastapi import APIRouter, HTTPException, Depends
from app.db.session import SessionDep
from app.utils.jwt_handler import jwt_required
from app.services.finance import FinanceEngine

# Define router
router = APIRouter()


@router.get("/report/{year}/{month}", status_code=200, response_model=dict)
async def get_report(
    year: int, month: int, session: SessionDep, payload: dict = Depends(jwt_required)
):
    """
    Allow user to get the report of how much they earned and spent
    :param year: The year of all transactions
    :param month: The month of transactions
    :param session: A workspace for interacting with db
    :param payload: Decoded JWT containing user claims (validated via jwt_required)
    :return a successfull msg including the report
    """
    # Get user id from the payload
    user_id = payload.get("sub")

    engine = FinanceEngine(db=session)

    report = engine.generate_monthly_report(user_id=user_id, month=month, year=year)

    return {"status": "success", "report": report}