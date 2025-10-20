from dataclasses import dataclass
from typing import List, Optional
from enum import Enum

class AuthStatus(Enum):
    PENDING = "pending"
    AUTHENTICATED = "authenticated"
    FAILED = "failed"

class TransactionStatus(Enum):
    PENDING = "pending"
    AUTHORIZED = "authorized"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class Product:
    id: str
    name: str
    price: float
    merchant: str
    description: str

@dataclass
class User:
    id: str
    name: str
    spending_limit: float
    available_balance: float

@dataclass
class Transaction:
    id: str
    user_id: str
    amount: float
    merchant: str
    product_id: str
    status: TransactionStatus
    auth_token: Optional[str] = None