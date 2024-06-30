from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import col, delete, func, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
    get_current_active_superuser,
)
from app.models import (Price, PriceList, PriceResponse)
import httpx


router = APIRouter()


@router.get(
    "/latest",
    dependencies=[Depends(get_current_active_superuser)],
)
def read_latest_price() -> Any:
    """
    """
    resp = httpx.get("https://prod-api.exgold.co.kr/api/v1/main/detail/domestic/price")

    resp.raise_for_status()
    
    return resp.json() 
