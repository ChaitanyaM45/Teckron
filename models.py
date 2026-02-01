from pydantic import BaseModel
from typing import Optional

class OrderRequest(BaseModel):
    # Defines the structure of an incoming customer order
    customer_name: str
    customer_email: str
    customer_phone: Optional[str] = None

    item_name: str
    quantity: int


class DecisionResponse(BaseModel):
    # Defines the structure of the decision response sent to the client
    decision: str
    reason: str

    customer_name: str
    customer_email: str

    assigned_staff: Optional[str] = None
    explanation: Optional[str] = None
