from bson import ObjectId
from fastapi import APIRouter, Request,HTTPException
from backend.app.core.llmhandler import LLMHandler
from backend.app.db import db, get_transaction_collection
from backend.app.schemas.transaction import TransactionSchema
from typing import List
from pymongo.collection import Collection
from datetime import datetime
from fastapi import Depends
from dateutil.relativedelta import relativedelta

router = APIRouter()

@router.post("/inbound-email")
async def handle_email(request: Request):
    payload = await request.json()
    email_body = payload.get("TextBody", "") or payload.get("HtmlBody", "")
    subject = payload.get("Subject", "")

    llm = LLMHandler()
    ai_response = llm.analyze_email(email_body)
    try:
        amount_value = ai_response["amount"]
        ai_response["amount"] = float(amount_value)
        

        # Validate with Pydantic
        transaction_data = TransactionSchema(**ai_response, created_at=datetime.now())

    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Invalid AI response: {e}")
    
    result = await db["transactions"].insert_one(transaction_data.dict())

    return {
        "message": "Transaction saved to MongoDB",
        "mongo_id": str(result.inserted_id)
    }

@router.get("/transactions", response_model=List[TransactionSchema])
async def list_transactions():
    cursor = db["transactions"].find()
    transactions = await cursor.to_list(length=1000)
    return transactions

@router.get("/transactions/banks", response_model=List[TransactionSchema])
async def list_bank_transactions():
    cursor = db["transactions"].find({"is_transaction": True})
    transactions = await cursor.to_list(length=1000)
    return transactions

@router.get("/transactions/high-confidence", response_model=List[TransactionSchema])
async def list_high_confidence_transactions():
    cursor = db["transactions"].find({"confidence": {"$gt": 90}})
    transactions = await cursor.to_list(length=1000)
    return transactions

def get_month_range():
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    if now.month == 12:
        end_of_month = datetime(now.year + 1, 1, 1)
    else:
        end_of_month = datetime(now.year, now.month + 1, 1)
    return start_of_month, end_of_month

@router.get("/monthly-spend")
async def check_monthly_spend(
    transactions: Collection = Depends(get_transaction_collection)
):
    now = datetime.now()
    start_of_month = datetime(now.year, now.month, 1)
    end_of_month = datetime(now.year, now.month + 1, 1) if now.month < 12 else datetime(now.year + 1, 1, 1)


    pipeline = [
        {
            "$match": {
                "is_transaction": True,
                "transaction_type": "debit",
                 "_id": {
                    "$gte": ObjectId.from_datetime(start_of_month),
                    "$lt": ObjectId.from_datetime(end_of_month)
                }
            }
        },
        {
            "$group": {
                "_id": None,
                "total_spent": {"$sum": "$amount"}
            }
        }
    ]

    cursor = transactions.aggregate(pipeline)
    spend_info = None
    async for doc in cursor:
        spend_info = doc

    monthly_limit = 50000  # Set your limit here
    total_spent = spend_info["total_spent"] if spend_info else 0

    return {
        "total_spent": total_spent,
        "monthly_limit": monthly_limit,
        "limit_reached": total_spent >= monthly_limit
    }

@router.get("/monthly-spend-history")
async def monthly_spend_history(
    transactions: Collection = Depends(get_transaction_collection)
):
    now = datetime.now()
    start_month = (now.replace(day=1) - relativedelta(months=5)).replace(hour=0, minute=0, second=0, microsecond=0)

    pipeline = [
        {
            "$match": {
                "is_transaction": True,
                "transaction_type": "debit",
                "created_at": {"$gte": start_month}
            }
        },
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$created_at"},
                    "month": {"$month": "$created_at"}
                },
                "total_spent": {"$sum": "$amount"}
            }
        },
        {
            "$sort": {"_id.year": 1, "_id.month": 1}
        }
    ]

    result = []
    async for doc in transactions.aggregate(pipeline):
        result.append({
            "month": f"{doc['_id']['year']}-{str(doc['_id']['month']).zfill(2)}",
            "total_spent": doc["total_spent"]
        })

    return result
