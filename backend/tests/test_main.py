import pytest
from fastapi.testclient import TestClient
from typing import List, Optional

from app.main import app
from app.infrastructure.api.routes import get_user_manager
from app.application.use_cases.user_manager import UserManager
from app.domain.ports.user_repository import UserRepository
from app.domain.models import User, UserCreate, UserUpdate

class MockUserRepository(UserRepository):
    def __init__(self):
        self.users = {}

    def create(self, user: User) -> User:
        self.users[user.id] = user
        return user

    def get_by_id(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_all(self) -> List[User]:
        return list(self.users.values())

    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        user = self.get_by_id(user_id)
        if not user:
            return None
        if user_update.name is not None:
            user.name = user_update.name
        if user_update.email is not None:
            user.email = user_update.email
        return user

    def delete(self, user_id: str) -> bool:
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

# Setup dependency override
mock_repo = MockUserRepository()
mock_manager = UserManager(repository=mock_repo)

def override_get_user_manager():
    return mock_manager

app.dependency_overrides[get_user_manager] = override_get_user_manager

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_before_and_after_tests():
    # Clear the mock repository before each test
    mock_repo.users = {}
    yield

def test_health_check():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "API running"}

def test_create_user():
    response = client.post(
        "/api/users",
        json={"name": "Alice Wonderland", "email": "alice@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice Wonderland"
    assert data["email"] == "alice@example.com"
    assert "id" in data

def test_get_user():
    # Arrange
    create_response = client.post(
        "/api/users",
        json={"name": "Bob Builder", "email": "bob@example.com"}
    )
    user_id = create_response.json()["id"]

    # Act
    get_response = client.get(f"/api/users/{user_id}")

    # Assert
    assert get_response.status_code == 200
    assert get_response.json() == create_response.json()

def test_list_users():
    # Arrange
    client.post("/api/users", json={"name": "User 1", "email": "user1@example.com"})
    client.post("/api/users", json={"name": "User 2", "email": "user2@example.com"})

    # Act
    response = client.get("/api/users")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "User 1"
    assert data[1]["name"] == "User 2"

def test_update_user():
    # Arrange
    create_response = client.post(
        "/api/users",
        json={"name": "Old Name", "email": "old@example.com"}
    )
    user_id = create_response.json()["id"]

    # Act
    update_response = client.put(
        f"/api/users/{user_id}",
        json={"name": "New Name"}
    )

    # Assert
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "old@example.com"

def test_delete_user():
    # Arrange
    create_response = client.post(
        "/api/users",
        json={"name": "To Delete", "email": "delete@example.com"}
    )
    user_id = create_response.json()["id"]

    # Act
    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 204

    # Assert get returns 404
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 404
