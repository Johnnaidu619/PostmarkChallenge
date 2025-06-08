from fastapi import HTTPException, status
from openai import OpenAI, OpenAIError
import os
import json
from dotenv import load_dotenv

load_dotenv()

DEFAULT_LLM_BASE_URL = "https://api.deepseek.com/v1"
DEFAULT_LLM_API_KEY = os.environ.get("LLM_API_KEY")
DEFAULT_LLM_MODEL_NAME = "deepseek-chat"

DEFAULT_PROMPT = """
You are an intelligent email parser.

Your job is to read the email content and determine if it represents a **bank transaction**.

Respond in this strict JSON format:
{
    "is_transaction": true/false,
    "bank_name": "Bank name if found, else null",
    "amount": number (only numeric value),
    "currency": "INR/USD/etc (without amount)",
    "transaction_type": "credit/debit/unknown",
    "description": "Short description or merchant name",
    "confidence": number from 0 to 100 (how confident you are in this being a transaction)"
}

Only respond in this JSON format. Do not explain anything.
Here is the email:
"""

class LLMHandler:
    def __init__(self, llm_base_url=None, llm_api_key=None, llm_model_name=None):
        print("Creating LLM Handler client")
        self.LLM_BASE_URL = llm_base_url or DEFAULT_LLM_BASE_URL
        self.LLM_API_KEY = llm_api_key or DEFAULT_LLM_API_KEY
        self.LLM_MODEL_NAME = llm_model_name or DEFAULT_LLM_MODEL_NAME
        try:
            print(self.LLM_API_KEY)
            self.LLM_CLIENT = OpenAI(
                base_url=self.LLM_BASE_URL,
                api_key=self.LLM_API_KEY
            )
        except Exception as e:
            print(f"Unable to create OpenAI client: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error initializing OpenAI client"
            )

    def analyze_email(self, email_text: str):
        print("💬 Analyzing email for bank transaction...")

        full_prompt = DEFAULT_PROMPT + "\n" + email_text

        try:
            response = self.LLM_CLIENT.chat.completions.create(
                model=self.LLM_MODEL_NAME,
                messages=[
                    {"role": "user", "content": full_prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            result = response.choices[0].message.content
            print(result)
            print("✅ AI response received")
            return json.loads(result)

        except OpenAIError as e:
            print(f"OpenAIError while analyzing email: {e}")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=str(e)
            )

        except Exception as e:
            print(f"Unhandled error during email analysis: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unexpected error during AI analysis"
            )
