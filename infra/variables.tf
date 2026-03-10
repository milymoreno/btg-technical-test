variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name for tagging and naming resources"
  type        = string
  default     = "btg-tech-test"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}
