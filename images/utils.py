import uuid
import boto3 as boto3
from backend.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def uploadBucket(path):
    data = open(path,'rb')  #버킷에 저장할 이미지 불러오기

    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY
    )
    image_type = "jpg"
    image_uuid = str(uuid.uuid4())
    s3_client.put_object(Body=data, Bucket='meet-the-past', Key=image_uuid + "." + image_type)
    image_url = "http://meet-the-past.s3.ap-northeast-2.amazonaws.com/" + \
                image_uuid + "." + image_type
    image_url = image_url.replace(" ", "/")
    return image_url