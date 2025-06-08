from typing import Collection
from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "email_insights")

client = AsyncIOMotorClient(MONGO_URL)
db = client[MONGO_DB_NAME]


def get_transaction_collection() -> Collection:
    return db["transactions"]

