from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
import uvicorn
from config import Settings
import os

app = FastAPI()

settings = None

@app.on_event("startup")
def load_settings():
    """Load latest environment variables when the app starts."""
    global settings
    settings = Settings()  # creates fresh instance using latest env vars



class pie(BaseModel) :
    id: int
    merchant: str
    owner: str

merchant_list: List[pie]= [
    pie(id=1, merchant="PieTech", owner="Alice"),
    pie(id=2, merchant="TechPies", owner="Bob")
]

@app.get("/")
def read_root():
    return {
        "message": settings.Message,       # <--- match the capitalization
        "admin_email": settings.admin_email
    }

@app.get("/merchants")
def get_merchant_list():
  return merchant_list

@app.get("/merchant/{pie_id}")
def get_merchant_list(pie_id: int):
  for merchant in merchant_list:
    if merchant.id == pie_id:
        return merchant
  return {"error": "Merchant not found"}

@app.post("/merchant")
def add_merchant(merchant_list: pie):
    merchant_list.append(merchant_list)
    return merchant_list

@app.put("/merchant/{pie_id}")
def update_merchant(pie_id: int, updated_merchant: pie):
    for index, merchant_list in enumerate(merchant_list):
        if merchant_list.id == pie_id:
            merchant_list[index] = updated_merchant
            return updated_merchant
    return {"error": "Merchant not found"}

@app.delete("/merchant/{pie_id}")
def delete_merchant(pie_id: int):
    for index, merchant_list in enumerate(merchant_list):
        if merchant_list.id == pie_id:
            del merchant_list[index]
            return {"message": "Merchant deleted"}
    return {"error": "Merchant not found"}