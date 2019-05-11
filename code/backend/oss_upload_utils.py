# coding=utf-8

"""
处理资源上传
"""
import os
import datetime
import oss2
from oss2 import determine_part_size, SizedFileAdapter
from oss2.models import PartInfo
import config
from common import mongodb
import mongodb_utils


class OssUtils(object):

    def __init__(self, resource_path):
        """
        :param resource_path: 资源的绝对路径
        """
        self.resource_num = 0
        self.resource_path = resource_path
        AccessKeyId = "LTAIuU3N2Gou4OXX"
        AccessKeySecret = "QVEIp0J7gVwrXVt7JhSVzTQiQdlDj0"
        BucketName = "daimayishu-source"
        auth = oss2.Auth(AccessKeyId, AccessKeySecret)
        self.bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', BucketName)

    def iter_and_upload_resource(self):
        """
        循环遍历文件夹所有文件，只遍历一层
        :return:
        """
        if os.path.isfile(self.resource_path):
            self.upload_resource(self.resource_path)
        else:
            list = os.listdir(self.resource_path)
            for line in list:
                file_path = os.path.join(self.resource_path, line)
                if os.path.isfile(file_path):
                    total_size = os.path.getsize(file_path)
                    if total_size < 50 * 1024 * 1024:
                        self.upload_resource(file_path)
                    else:
                        print("{0}{1}".format(file_path, "不上传,因为文件大于50M"))
                else:
                    continue
        print("{0}{1}{2}".format("共上传", str(self.resource_num), "个"))

    @staticmethod
    def get_file_name(file_path):
        """
        获取文件名称
        :param file_path:
        :return:
        返回文件名
        """
        filename = os.path.split(file_path)[1];
        extension = os.path.splitext(filename)[1];
        if extension[1:] not in ["pdf"]:
            print("{0}{1}".format(file_path, "不上传"))
            return None
        else:
            print("{0}{1}{2}".format(str(datetime.datetime.now()), file_path, "正在上传"))
            return filename

    def upload_resource(self, file_path):
        """
        向阿里云oss上传文件
        :param file_path: 待上传的文件路径
        :return:
        """
        filename = self.get_file_name(file_path)
        if filename:
            try:
                filters = {"title": filename}
                pdf_obj = mongodb_utils.find_one_resource(filters)
                if pdf_obj is None:
                    # self.bucket.put_object_from_file(filename, file_path)
                    self.split_file_upload(file_path, filename)
                    mongodb_utils.insert_one_resource({"title": filename})
                    self.resource_num += 1
                    print("{0}{1}{2}".format(str(datetime.datetime.now()), file_path, "上传完成"))
                else:
                    print("{0}{1}{2}".format(str(datetime.datetime.now()), file_path, "已存在"))
            except Exception as err:
                print err.message
                print("{0}{1}{2}".format(str(datetime.datetime.now()), file_path, "上传失败"))

    def percentage(self, consumed_bytes, total_bytes):
        if total_bytes:
            rate = int(100 * (float(consumed_bytes) / float(total_bytes)))
            print '\r{0}% '.format(rate)

    def split_file_upload(self, file_path, filename):
        """
        分片上传文件
        :param file_path:
        :param filename:
        :return:
        """
        total_size = os.path.getsize(file_path)

        # determine_part_size方法用来确定分片大小。
        part_size = determine_part_size(total_size, preferred_size=10 * 1024 * 1024)

        # 初始化分片。
        upload_id = self.bucket.init_multipart_upload(filename).upload_id
        parts = []
        # 逐个上传分片。
        with open(file_path, 'rb') as fileobj:
            part_number = 1
            offset = 0
            while offset < total_size:
                num_to_upload = min(part_size, total_size - offset)
                # SizedFileAdapter(fileobj, size)方法会生成一个新的文件对象，重新计算起始追加位置。
                result = self.bucket.upload_part(filename, upload_id, part_number,
                                                 SizedFileAdapter(fileobj, num_to_upload),
                                                 progress_callback=self.percentage)
                parts.append(PartInfo(part_number, result.etag))

                offset += num_to_upload
                part_number += 1

        # 完成分片上传。
        self.bucket.complete_multipart_upload(filename, upload_id, parts)


if __name__ == "__main__":
    raw_file_path = "/root/pdf"
    aliyun_host = "47.112.100.1"
    aliyun_port = 27017
    aliyun_db = "daimayishu"
    # 注册数据库对象
    # mongodb.register_mongo_client(config.TEST_MONGO_HOST,
    #                               int(config.TEST_MONGO_PORT),
    #                               config.TEST_MONGO_DATABASE)
    mongodb.register_mongo_client(aliyun_host,
                                  aliyun_port,
                                  aliyun_db)
    oss_util = OssUtils(raw_file_path)
    oss_util.iter_and_upload_resource()
