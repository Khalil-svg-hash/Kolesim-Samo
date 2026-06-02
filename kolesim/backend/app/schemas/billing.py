from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class SubscribeRequest(BaseModel):
    plan: Literal["monthly", "annual"]


class SubscribeResponse(BaseModel):
    payment_url: str


class SubscriptionResponse(BaseModel):
    id: UUID
    user_id: UUID
    plan: str
    status: str
    amount_rub: float
    started_at: datetime
    expires_at: datetime
