from pydantic import BaseModel

class PaymentRequest(BaseModel):
    name: str
    email: str
    address: str
    amount: float