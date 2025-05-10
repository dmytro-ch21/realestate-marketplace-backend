from app.repositories.listing_repository import ListingRepository
from app.models.listing import Listing
from typing import Optional, List, Dict, Any


class ListingService:
    @staticmethod
    def create_listing(owner_id: int, title: str, price: float, data: Dict[str, Any]) -> Listing:
        extra_data = {key: value for key, value in data.items() if key not in ("owner_id", "title", "price")}
        return ListingRepository.create(
            owner_id=owner_id,
            title=title,
            price=price,
            additional_data=extra_data
        )
    
    @staticmethod
    def get_all_listings() -> List[Listing]:
        return ListingRepository.get_all()