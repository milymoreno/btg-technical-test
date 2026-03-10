resource "aws_dynamodb_table" "users_table" {
  name           = "${var.project_name}-${var.environment}-users"
  billing_mode   = "PAY_PER_REQUEST" # Free tier friendly / serverless
  hash_key       = "id"

  attribute {
    name = "id"
    type = "S"
  }

  tags = {
    Name        = "UsersTable"
    Environment = var.environment
    Project     = var.project_name
  }
}
