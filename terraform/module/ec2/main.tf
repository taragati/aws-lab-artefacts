resource "aws_vpc" "my_vpc" {
  cidr_block = "172.16.0.0/16"

  tags = {
    Name = "tf-example"
  }
}

resource "aws_subnet" "my_subnet" {
  vpc_id            = aws_vpc.my_vpc.id
  cidr_block        = "172.16.10.0/24"
  availability_zone = "us-east-1a"

  tags = {
    Name = "tf-example"
  }
}

resource "aws_instance" "foo" {
  ami           = "ami-08b5b3a93ed654d19" # us-east-1
  instance_type = "t2.micro"
  subnet_id = aws_subnet.my_subnet.id

  credit_specification {
    cpu_credits = "unlimited"
  }
}
