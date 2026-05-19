import logging
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AddressCreate, AddressUpdate, AddressResponse
from app.services import (
    create_address,
    get_address,
    update_address,
    delete_address,
    get_addresses_within_distance
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.post("/", response_model=AddressResponse, status_code=201)
def create(payload: AddressCreate, db: Session = Depends(get_db)):
    logger.info("POST /addresses - creating new address")
    return create_address(db, payload)


@router.get("/nearby", response_model=list[AddressResponse])
def nearby(
    latitude: float = Query(..., description="Center latitude"),
    longitude: float = Query(..., description="Center longitude"),
    distance_km: float = Query(..., description="Radius in kilometers"),
    db: Session = Depends(get_db)
):
    logger.info(f"GET /addresses/nearby - lat={latitude}, lon={longitude}, distance={distance_km}km")
    return get_addresses_within_distance(db, latitude, longitude, distance_km)


@router.get("/{address_id}", response_model=AddressResponse)
def read(address_id: int, db: Session = Depends(get_db)):
    logger.info(f"GET /addresses/{address_id}")
    address = get_address(db, address_id)
    if not address:
        logger.warning(f"Address {address_id} not found")
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.put("/{address_id}", response_model=AddressResponse)
def update(address_id: int, payload: AddressUpdate, db: Session = Depends(get_db)):
    logger.info(f"PUT /addresses/{address_id}")
    address = update_address(db, address_id, payload)
    if not address:
        logger.warning(f"Address {address_id} not found for update")
        raise HTTPException(status_code=404, detail="Address not found")
    return address


@router.delete("/{address_id}", status_code=204)
def delete(address_id: int, db: Session = Depends(get_db)):
    logger.info(f"DELETE /addresses/{address_id}")
    success = delete_address(db, address_id)
    if not success:
        logger.warning(f"Address {address_id} not found for deletion")
        raise HTTPException(status_code=404, detail="Address not found")