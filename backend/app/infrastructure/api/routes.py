from typing import List
from fastapi import APIRouter, HTTPException, Depends
from app.domain.models import User, UserCreate, UserUpdate
from app.application.use_cases.user_manager import UserManager
from app.infrastructure.adapters.dynamodb_repository import DynamoDBUserRepository

router = APIRouter()

def get_user_manager():
    # Dependency Injection: Instantiate adapter and inject it into Use Case
    repo = DynamoDBUserRepository()
    return UserManager(repository=repo)

@router.post("/users", response_model=User, status_code=201, summary="Create a new user")
def create_user(user: UserCreate, manager: UserManager = Depends(get_user_manager)):
    """
    Create a new user with name and email. The ID will be generated automatically.
    """
    return manager.create_user(user)

@router.get("/users", response_model=List[User], summary="Get all users")
def list_users(manager: UserManager = Depends(get_user_manager)):
    """
    Retrieve a list of all existing users.
    """
    return manager.list_users()

@router.get("/users/{user_id}", response_model=User, summary="Get a user by ID")
def get_user(user_id: str, manager: UserManager = Depends(get_user_manager)):
    """
    Retrieve a specific user by their ID.
    """
    user = manager.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=User, summary="Update a user")
def update_user(user_id: str, user_update: UserUpdate, manager: UserManager = Depends(get_user_manager)):
    """
    Update specific fields (name, email) of an existing user.
    """
    updated_user = manager.update_user(user_id, user_update)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@router.delete("/users/{user_id}", status_code=204, summary="Delete a user")
def delete_user(user_id: str, manager: UserManager = Depends(get_user_manager)):
    """
    Delete a user by their ID.
    """
    success = manager.delete_user(user_id)
    if not success:
        # In a generic implementation, true/false can signify if item existed
        pass 
    return None
