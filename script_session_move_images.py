import boto3

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

# Move used images to /old dir
# Copy objects
print("Moving images to /old directory ...")
deleteThis = []
for item in res["Contents"]:
    key = item["Key"]
    if key != prefix: # Ignore the root dir
        copy_source = {
            'Bucket': BUCKET_NAME,
            'Key': key
        }
        filename = key.replace(prefix, "")
        oldpath = f"old/{filename}"
        client.copy(copy_source, BUCKET_NAME, oldpath)
        print("Copied")

deleteThis = []
for item in res["Contents"]:
    key = item["Key"]
    if key != prefix: # Ignore the root dir
        deleteThis.append({'Key':key})

# Delete objects in /new
print(deleteThis)
response = client.delete_objects(
    Bucket=BUCKET_NAME,
    Delete={
        'Objects': deleteThis
    }
)
print(response)
print("Successfully moved processed images to /old directory.")