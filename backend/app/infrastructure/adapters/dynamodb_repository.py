import boto3
import os
from typing import List, Optional
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError
from app.domain.models import User, UserUpdate
from app.domain.ports.user_repository import UserRepository

class DynamoDBUserRepository(UserRepository):
    def __init__(self, table_name: str = None):
        region = os.getenv("AWS_REGION", "us-east-1")
        # In actual deployment, role handles auth. For local test, consider endpoint_url.
        endpoint_url = os.getenv("DYNAMODB_ENDPOINT_URL", None)
        # Use fallback fake credentials in case they run uvicorn locally without env vars set
        aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID", "fakeMyKeyId")
        aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY", "fakeSecretAccessKey")

        self.dynamodb = boto3.resource(
            'dynamodb', 
            region_name=region, 
            endpoint_url=endpoint_url,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )
        self.table_name = table_name or os.getenv("DYNAMODB_TABLE_NAME", "Users")
        self.table = self.dynamodb.Table(self.table_name)

    def create(self, user: User) -> User:
        try:
            self.table.put_item(Item=user.model_dump())
            return user
        except ClientError as e:
            print(f"Error creating user: {e}")
            raise

    def get_by_id(self, user_id: str) -> Optional[User]:
        try:
            response = self.table.get_item(Key={'id': user_id})
            item = response.get('Item')
            if item:
                return User(**item)
            return None
        except ClientError as e:
            print(f"Error getting user: {e}")
            raise

    def get_all(self) -> List[User]:
        try:
            response = self.table.scan()
            items = response.get('Items', [])
            return [User(**item) for item in items]
        except ClientError as e:
            print(f"Error scanning users: {e}")
            raise

    def update(self, user_id: str, user_update: UserUpdate) -> Optional[User]:
        update_expr = "SET "
        expr_attr_values = {}
        expr_attr_names = {}
        
        update_data = user_update.model_dump(exclude_unset=True)
        if not update_data:
            return self.get_by_id(user_id) # Nothing to update
            
        for key, value in update_data.items():
            update_expr += f"#{key} = :{key}, "
            expr_attr_names[f"#{key}"] = key
            expr_attr_values[f":{key}"] = value

        update_expr = update_expr.rstrip(', ')

        try:
            response = self.table.update_item(
                Key={'id': user_id},
                UpdateExpression=update_expr,
                ExpressionAttributeNames=expr_attr_names,
                ExpressionAttributeValues=expr_attr_values,
                ReturnValues="ALL_NEW"
            )
            return User(**response.get('Attributes', {}))
        except ClientError as e:
            # Catch condition where item doesn't exist if we added a constraint,
            # though standard update_item creates it if it doesn't exist unless specified.
            print(f"Error updating user: {e}")
            # For strictness, if checking existence first:
            return None

    def delete(self, user_id: str) -> bool:
        try:
            response = self.table.delete_item(
                Key={'id': user_id},
                ReturnValues="ALL_OLD"
            )
            # Check if item existed
            if 'Attributes' in response:
                return True
            return False # Depending on logic, might just return True always if we assume idempotency
        except ClientError as e:
            print(f"Error deleting user: {e}")
            return False
