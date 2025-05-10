from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository

class UserService:
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[User]:
       return UserRepository.get_by_id(user_id)

    @staticmethod
    def update_user(user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return UserRepository.update(user)