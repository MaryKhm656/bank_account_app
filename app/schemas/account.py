from pydantic import BaseModel, ConfigDict

class BankAccountCreate(BaseModel):
    owner: str
    pin: str
    balance: float = 0.0

class BankAccountOut(BaseModel):
    id: int
    owner: str
    balance: float

    model_config = ConfigDict(from_attributes=True)
    
    
class DepositRequest(BaseModel):
    amount: float
    pin: str
    
class WithdrawRequest(BaseModel):
    amount: float
    pin: str
    
class TransferRequest(BaseModel):
    amount: float
    pin: str