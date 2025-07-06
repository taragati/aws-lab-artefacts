resource "aws_s3_bucket" "example" {
  bucket = "niranjan-2025"

  tags = {
    Name        = "Environment"
    Environment = "Dev"
  }
}