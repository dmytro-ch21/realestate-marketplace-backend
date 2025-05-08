from typing import Optional, List
from app.extensions import db
from app.models.listing import Listing
from sqlalchemy import select


class ListingRepository:
    @staticmethod
    def create(owner_id: int, title: str, price: float, **kwargs) -> Listing:
        listing = Listing(owner_id=owner_id, title=title, price=price) # type: ignore
        # set all additional attributes
        for key, value in kwargs.items():
            if hasattr(listing, key):
                setattr(listing, key, value)
                
        db.session.add(listing)
        db.session.commit()
        return listing
    
    @staticmethod
    def get_by_id(listing_id: int) -> Optional[Listing]:
        stmt = select(Listing).where(Listing.id == listing_id)
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def get_by_owner_id(owner_id: int) -> List[Listing]:
        stmt = select(Listing).where(Listing.owner_id == owner_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())
    
    @staticmethod
    def update(listing: Listing) -> Listing:
        db.session.commit()
        return listing
    
    @staticmethod
    def delete(listing: Listing) -> bool:
        db.session.delete(listing)
        db.session.commit()
        return True
        
        
        