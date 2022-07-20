# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
import boto3
import os

BUCKET_NAME = "ecs-demo-1234"
REGION = "us-east-1"

# Using default profile (attached role)
session = boto3.Session(region_name = REGION)
client = session.client('s3')

# Get buckets with prefix
prefix = "new/"
res = client.list_objects_v2(
    Bucket=BUCKET_NAME,
    Prefix=prefix
)

# Create dir
path = f'{os.getcwd()}/tmp'
isExist = os.path.exists(path)
if not isExist:
    os.mkdir(path)

# Download all contents in the bucket with the prefix /new
for item in res["Contents"]:
    key = item["Key"]
    if key != prefix: # Ignore the root dir
        filename = key.replace(prefix, "")
        client.download_file(BUCKET_NAME, key, f"{path}/{filename}")
