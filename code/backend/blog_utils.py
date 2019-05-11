# coding=utf-8

"""
博客管理端
"""
import config
import json
from common import mongodb
import mongodb_utils
import sys

reload(sys)

sys.setdefaultencoding('utf8')

mongodb.register_mongo_client(config.TEST_MONGO_HOST,
                              int(config.TEST_MONGO_PORT),
                              config.TEST_MONGO_DATABASE)

blog_update_catagory_path = "/root/blog/blog.json"

with open(blog_update_catagory_path, "r") as blog_obj:
    content = json.load(blog_obj)
    for blog in content["blog"]:
        title = blog["title"]
        category = blog["category"]
        description = blog["description"]
        filters = {"title": title, "category": category}
        blog_record = mongodb_utils.find_one_blog(filters)
        if blog_record:
            print("{0}已经存在！".format(title))
        else:
            mongodb_utils.insert_one_blog(blog)
            print("{0}记录成功！".format(blog['title']))
