from fastapi import APIRouter, HTTPException
from app.schemas.account import BankAccountCreate, BankAccountOut, DepositRequest
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


@router.post("/accounts/{account_id}/deposit")
def deposit_to_account(account_id: int, request: DepositRequest):
    try:
        account = functions.deposit_to_account(
            account_id=account_id,
            amount=request.amount,
            pin=request.pin
        )
        return {"message": f"Счет успешно пополнен! Новый баланс: {account.balance}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Ошибка при работе с базой данных")

