terraform {
    required_providers {
      aws = {
        source = "hashicorp/aws"
        version = "~> 4.0.0"
      }
    }
}

provider "aws" {
    region = "us-east-1"
    access_key = "your_aws_access_key"
    secret_key = "your_aws_secret_access_key"
}

resource "aws_s3_bucket" "example" {
  bucket = "niranjan-123234242"

  tags = {
    Name        = "Environment"
    Environment = "Dev"
  }
}
