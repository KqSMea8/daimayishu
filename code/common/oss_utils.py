# coding=utf-8

"""
处理阿里云资源
"""
import oss2

AccessKeyId = "LTAIuU3N2Gou4OXX"
AccessKeySecret = "QVEIp0J7gVwrXVt7JhSVzTQiQdlDj0"
BucketName = "daimayishu-source"
auth = oss2.Auth(AccessKeyId, AccessKeySecret)
bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', BucketName)


def get_url(resource_name, live_time=120):
    return bucket.sign_url('GET', resource_name, live_time)
