from fastapi import APIRouter
from pydantic import BaseModel
from app.services.brand_service import BrandRiskService

router = APIRouter()

service = BrandRiskService("app/models/brand_model.pkl")

class BrandRequest(BaseModel):
    brand_name: str
    domain: str


@router.post("/brand-risk")
def brand_risk(request: BrandRequest):
    return service.evaluate(request.brand_name, request.domain)