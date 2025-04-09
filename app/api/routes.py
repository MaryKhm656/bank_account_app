from fastapi import APIRouter, HTTPException
from app.schemas.account import BankAccountCreate, BankAccountOut
from app import models
from app.database import SessionLocal
from app import functions
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/accounts/", response_model=BankAccountOut)
def create_account(account: BankAccountCreate):
    created = functions.create_account(
        owner=account.owner,
        pin=account.pin,
        initial_balance=account.balance
    )
    return created


@router.get("/accounts/{account_id}", response_model=BankAccountOut)
def get_account_by_id(account_id: int, pin: str):
    try:
        account = functions.get_account_by_id(
            account_id=account_id,
            pin=pin
        )
        return account
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Ошибка при работе с базой данных")

