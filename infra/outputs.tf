output "alb_dns_name" {
  description = "DNS Name of the Application Load Balancer"
  value       = aws_lb.main_alb.dns_name
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB users table"
  value       = aws_dynamodb_table.users_table.name
}

output "ecr_backend_url" {
  description = "URL of the backend ECR repository"
  value       = aws_ecr_repository.backend.repository_url
}

output "ecr_frontend_url" {
  description = "URL of the frontend ECR repository"
  value       = aws_ecr_repository.frontend.repository_url
}
