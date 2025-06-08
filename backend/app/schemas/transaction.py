from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TransactionSchema(BaseModel):
    is_transaction: bool
    bank_name: Optional[str]
    amount: float
    currency: str
    transaction_type: str
    description: str
    confidence: int
    created_at: Optional[datetime] = datetime.now()

