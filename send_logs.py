import boto3

s3 = boto3.client('s3')
BUCKET_NAME = "791-options-data"

s3.upload_file("logs.txt", "791-options-data", "logs.txt")
