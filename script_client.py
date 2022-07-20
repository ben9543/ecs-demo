# https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html

from time import sleep
import boto3
import requests
import os
import json

# SSM Parameter Store
# /demo/ecs/access-key
# /demo/ecs/secret-key
TASKROLE_ENV = "AWS_CONTAINER_CREDENTIALS_RELATIVE_URI"
ACCESS_KEY = ""
SECRET_KEY = ""

print(os.environ)
print(os.environ[TASKROLE_ENV])
if(TASKROLE_ENV in dict(os.environ)):
    relative_path = os.environ[TASKROLE_ENV]
    url = f"http://169.254.170.2{relative_path}"
    r = requests.get(url)
    r = r.json()
    print(r)
    '''
    r = requests.get(os.environ['ECS_CONTAINER_METADATA_URI'])
    r = r.json()
    print(r)
    r = requests.get(os.environ['ECS_CONTAINER_METADATA_URI_V4'])
    r = r.json()
    print(r)
    '''
    ACCESS_KEY = r['AccessKeyId']
    SECRET_KEY = r['SecretAccessKey']
else:
    ACCESS_KEY = os.environ['AWS_ACCESS_KEY_ID']
    SECRET_KEY = os.environ['AWS_SECRET_ACCESS_KEY']
BUCKET_NAME = "ecs-demo-1234"
REGION = "us-east-1"

client = boto3.client(
    's3',
    aws_access_key_id=ACCESS_KEY,
    aws_secret_access_key=SECRET_KEY,
    region_name = REGION
)

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

# Process image (sleep for 5 mins)
print("Processing the image ...")
sleep(5*60)
##### You can do whatever you want to do with the images here #####
print("Image processing is done!")


# Move used images to /old dir
# Copy objects
print("Moving images to /old directory ...")
deleteThis = []
for item in res["Contents"]:
    key = item["Key"]
    if key != prefix: # Ignore the root dir
        deleteThis.append({'Key':key})
        copy_source = {
            'Bucket': BUCKET_NAME,
            'Key': key
        }
        filename = key.replace(prefix, "")
        oldpath = f"old/{filename}"
        # print(oldpath)
        client.copy(copy_source, BUCKET_NAME, oldpath)
        print("Copied")

# Delete objects in /new
response = client.delete_objects(
    Bucket=BUCKET_NAME,
    Delete={
        'Objects': deleteThis
    }
)
print("Successfully moved processed images to /old directory.")