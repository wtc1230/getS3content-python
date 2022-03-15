"""
Requirement:
1. List of S3 buckets within your accounts.
The output should be a Python "list of dictionary" and each dictionary item should contain the following:
2. Name of S3 bucket:
3. URL of the bucket:
4. Encrypted: True/False
"""
import boto3
from botocore.exceptions import ClientError


# create a s3 client in ap-east-1
def ap_east_client():
    return boto3.client('s3', region_name='ap-east-1')


# create a s3 client in us-east-1
def s3_client():
    return boto3.client('s3', region_name='us-east-1')


# list all the buckets from the AWS account
def list_buckets():
    return s3_client().list_buckets()


# check for the s3 bucket is encrypted or not
def enc_check(name):
    encrypted = "True"
    try:
        # get the encryption information for the bucket
        # if not error message occurs when getting the encryption information of bucket, return encrypted = Ture
        s3_client().get_bucket_encryption(Bucket=name)
    except ClientError as e:
        # if this error occurs, means the default region(us-east-1) is incompatible with the bucket
        if e.response['Error']['Code'] == 'IllegalLocationConstraintException':
            try:
                # change the region to ap-east-1, if no error message return encrypted = Ture
                ap_east_client().get_bucket_encryption(Bucket=name)
            except ClientError as e:
                # if this error occurs, means the s3 bucket is not encrypted
                if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                    encrypted = "False"
        else:
            if e.response['Error']['Code'] == 'ServerSideEncryptionConfigurationNotFoundError':
                encrypted = "False"
            else:
                # display an unexpected error
                print('Bucket: ', name, ', unexpected error: ', e)
    return encrypted


# create a list of dictionary to contain the information of s3 buckets
content = []
for bucket_info in list_buckets().get('Buckets'):
    bucket_name = bucket_info.get('Name')
    s3_url = 'http://s3.amazonaws.com/' + bucket_info.get('Name') + '/'
    info = {
        "Name of S3 bucket: ": bucket_info.get('Name'),
        "URL of the bucket: ": s3_url,
        "Encrypted: ": enc_check(bucket_name)
    }
    # push the data into the dictionary
    content.append(info)

print(content)
