from typing import Optional, List
from app.extensions import db
from app.models.listing_image import ListingImage
from sqlalchemy import select


class ListingImageRepository:
    @staticmethod
    def create(listing_id: int, image_url: str, cl_pid: str, **kwargs) -> ListingImage:
        image = ListingImage(listing_id=listing_id, image_url=image_url, claudinary_public_id=cl_pid) # type: ignore
        # set optional attributes
        for key, value in kwargs.items():
            if hasattr(image, key):
                setattr(image, key, value)
        
        db.session.add(image)
        db.session.commit()
        return image
    
    @staticmethod
    def get_by_id(image_id: int) -> Optional[ListingImage]:
        stmt = select(ListingImage).where(ListingImage.id == image_id)
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def get_by_listing(listing_id: int) -> List[ListingImage]:
        stmt = select(ListingImage).where(ListingImage.listing_id == listing_id)
        results = db.session.execute(stmt)
        return list(results.scalars().all())
    
    @staticmethod
    def get_primary_image(listing_id: int) -> Optional[ListingImage]:
        stmt = select(ListingImage).where(
            ListingImage.listing_id == listing_id,
            ListingImage.is_primary == True
        )
        result = db.session.execute(stmt)
        return result.scalars().first()
    
    @staticmethod
    def delete(image: ListingImage) -> bool:
        db.session().delete(image)
        db.session().commit()
        return True
        
    @staticmethod
    def upadate(image: ListingImage) -> ListingImage:
        db.session().commit()
        return image
    