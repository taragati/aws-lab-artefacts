resource "aws_s3_bucket" "example" {
  bucket = "niranjan-123234242"

  tags = {
    Name        = "Environment"
    Environment = "Dev"
  }
}