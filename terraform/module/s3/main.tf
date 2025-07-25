terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 5.92.0"
      }
    }
}

provider "aws" {
    region = "us-east-1"
    access_key = "your_aws_access_key"
    secret_key = "your_aws_secret_access_key"
}

resource "aws_s3_bucket" "example" {
  bucket = "niranjan-2025"

  tags = {
    Name        = "Environment"
    Environment = "Dev"
  }
}
