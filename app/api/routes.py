from fastapi import APIRouter, HTTPException
from app.schemas.account import BankAccountCreate, BankAccountOut, DepositRequest, WithdrawRequest, TransferRequest
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
    except SQLAlchemyError:
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

@router.post("/accounts/{account_id}/withdraw")
def withdraw_from_account(account_id: int, request: WithdrawRequest):
    try:
        account = functions.withdraw_from_account(
            account_id=account_id,
            amount=request.amount,
            pin=request.pin
        )
        return {"message": f"Снятие прошло успешно! Новый баланс: {account.balance}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Ошибка при работе с базой данных")
    
@router.post("/accounts/{from_id}/{to_id}/transfer")
def transfer_money_to_account(from_id: int, to_id: int, request: TransferRequest):
    try:
        to_account, from_account = functions.transfer_money(
            from_id=from_id,
            to_id=to_id,
            amount=request.amount,
            pin=request.pin
        )
        return {"message": f"Перевод выполнен успешно! Баланс {to_account.owner}: {to_account.balance}. Баланс {from_account.owner}: {from_account.balance}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Ошибка при работе с базой данных")
    
@router.delete("/accounts/delete/{account_id}")
def delete_account(account_id: int, pin: str):
    try:
        message = functions.delete_account(
            account_id=account_id,
            pin=pin
        )
        return {"message": message}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Ошибка при работе с базой данных")