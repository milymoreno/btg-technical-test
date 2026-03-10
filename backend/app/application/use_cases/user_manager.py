from typing import List, Optional
import uuid
from app.domain.models import User, UserCreate, UserUpdate
from app.domain.ports.user_repository import UserRepository

class UserManager:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, user_in: UserCreate) -> User:
        user = User(
            id=str(uuid.uuid4()),
            name=user_in.name,
            email=user_in.email
        )
        return self.repository.create(user)

    def get_user(self, user_id: str) -> Optional[User]:
        return self.repository.get_by_id(user_id)

    def list_users(self) -> List[User]:
        return self.repository.get_all()

    def update_user(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        return self.repository.update(user_id, user_update)

    def delete_user(self, user_id: str) -> bool:
        return self.repository.delete(user_id)
