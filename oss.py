import oss2
from config import ossConfig

endpoint = ossConfig['endpoint']
auth = oss2.Auth(ossConfig['key'], ossConfig['secret'])
bucket = oss2.Bucket(auth, endpoint, ossConfig['bucket'])

# Upload

def upload(ossPath, localPath):
    with open(oss2.to_unicode(localPath), 'rb') as f:
        bucket.put_object(ossPath, f)