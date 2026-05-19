import logging
from sqlalchemy.orm import Session
from geopy.distance import geodesic
from app.models import Address
from app.schemas import AddressCreate, AddressUpdate

logger = logging.getLogger(__name__)


def create_address(db: Session, payload: AddressCreate) -> Address:
    """Create and persist a new address record."""
    try:
        address = Address(**payload.model_dump())
        db.add(address)
        db.commit()
        db.refresh(address)
        logger.info(f"Address created successfully with id={address.id}")
        return address
    except Exception as e:
        logger.error(f"Failed to create address: {e}")
        db.rollback()
        raise


def get_address(db: Session, address_id: int) -> Address | None:
    """Retrieve a single address by ID. Returns None if not found."""
    address = db.query(Address).filter(Address.id == address_id).first()
    if address:
        logger.info(f"Address id={address_id} retrieved successfully")
    else:
        logger.warning(f"Address id={address_id} not found")
    return address


def update_address(db: Session, address_id: int, payload: AddressUpdate) -> Address | None:
    """Update an existing address. Only applies fields explicitly provided in the payload."""
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            logger.warning(f"Address id={address_id} not found for update")
            return None
        updates = payload.model_dump(exclude_unset=True)
        for field, value in updates.items():
            setattr(address, field, value)
        db.commit()
        db.refresh(address)
        logger.info(f"Address id={address_id} updated successfully")
        return address
    except Exception as e:
        logger.error(f"Failed to update address id={address_id}: {e}")
        db.rollback()
        raise


def delete_address(db: Session, address_id: int) -> bool:
    """Delete an address by ID. Returns True if deleted, False if not found."""
    try:
        address = db.query(Address).filter(Address.id == address_id).first()
        if not address:
            logger.warning(f"Address id={address_id} not found for deletion")
            return False
        db.delete(address)
        db.commit()
        logger.info(f"Address id={address_id} deleted successfully")
        return True
    except Exception as e:
        logger.error(f"Failed to delete address id={address_id}: {e}")
        db.rollback()
        raise


def get_addresses_within_distance(
    db: Session,
    latitude: float,
    longitude: float,
    distance_km: float
) -> list[Address]:
    """Return all addresses within a given distance (km) from the specified coordinates."""
    center = (latitude, longitude)
    all_addresses = db.query(Address).all()
    nearby = [
        address for address in all_addresses
        if geodesic(center, (address.latitude, address.longitude)).km <= distance_km
    ]
    logger.info(
        f"Found {len(nearby)} address(es) within {distance_km}km "
        f"of ({latitude}, {longitude})"
    )
    return nearby