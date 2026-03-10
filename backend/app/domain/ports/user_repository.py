from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.models import User, UserCreate, UserUpdate

class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[User]:
        pass

    @abstractmethod
    def get_all(self) -> List[User]:
        pass

    @abstractmethod
    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        pass

    @abstractmethod
    def delete(self, user_id: str) -> bool:
        pass
