# coding=utf-8
"""
代码艺术后端所有的数据库操作逻辑都在这里
"""
from common import mongodb
import datetime
import time
import uuid

db_name = {"user": "users", "resource": "resource", "blog": "blog", "advisory": "advisory", "pluralism": "pluralism"
    , "access": "access", "spider": "spider"}


def find_one_user(filters=None):
    """
    根据用户名查找用户
    :param username:
    :return:
    """
    user = mongodb.query_one(db_name["user"], filters)
    if user is None:
        raise Exception(u"用戶不存在")
    return user


def insert_one_user(doc=None):
    """
    添加用户
    :param doc:
    :return:
    """
    return mongodb.insert_one(db_name["user"], doc)


def update_one_user(filter):
    """
    记录用户登录时间
    :param filter:
    :return:

    """
    doc = {}
    last_login_time = datetime.datetime.now()
    doc["last_login_time"] = last_login_time
    mongodb.update_one(db_name["user"], filter, doc)


def insert_one_resource(doc=None):
    """
    添加资源
    :param doc:
    :return:
    """
    doc["upload_time"] = datetime.datetime.now()
    return mongodb.insert_one(db_name["resource"], doc)


def find_one_resource(filters=None):
    """
    根据书名查找书籍
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["resource"], filters)
    return resource


def find_many_resource(filters, skip, limit):
    """
    根据关键词查找书籍
    :param filters
    :param skip
    :param limit
    :return:
    """
    cursor = mongodb.query_many(db_name["resource"], filters=filters, skip=skip, limit=limit)
    return cursor


def update_one_resource(filter, doc):
    """
    记录资源下载次数
    :param filter:
    :return:

    """
    mongodb.update_one(db_name["resource"], filter, doc)


def find_one_blog(filters=None):
    """
    根据标题名称查找书籍
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["blog"], filters)
    return resource


def insert_one_blog(doc=None):
    """
    添加博客
    :param doc:
    :return:
    """
    doc["upload_time"] = datetime.datetime.now()
    return mongodb.insert_one(db_name["blog"], doc)


def find_many_blog(filters, skip, limit):
    """
    根据关键词查找书籍
    :param filters
    :param skip
    :param limit
    :return:
    """
    cursor = mongodb.query_many(db_name["blog"], filters=filters, skip=skip, limit=limit)
    return cursor


def find_all_blog():
    """
    根据关键词查找书籍
    :return:
    """
    cursor = mongodb.query_all(db_name["blog"])
    return cursor


def update_one_blog(filter, doc):
    """
    记录博客查询次数
    :param filter:
    :return:

    """
    mongodb.update_one(db_name["blog"], filter, doc)


def insert_one_advisory(doc=None):
    """
    添加咨询
    :param doc:
    :return:
    """
    doc["upload_time"] = datetime.datetime.now()
    doc["is_answer"] = 0
    doc["title"] = str(uuid.uuid4())
    return mongodb.insert_one(db_name["advisory"], doc)


def find_not_answer_advisory():
    """
    查找待回答的咨詢
    :return:
    """
    cursor = mongodb.query_many(db_name["advisory"], {"is_answer": 0}, 0, 0)
    return cursor


def update_one_advisory(filter, doc):
    """
    记录资源下载次数
    :param filter:
    :return:

    """
    mongodb.update_one(db_name["advisory"], filter, doc)


def find_answer_advisory(skip, limit):
    """
    查找待回答的咨詢
    :return:
    """
    cursor = mongodb.query_many(db_name["advisory"], {"is_answer": 1}, skip, limit)
    return cursor


def find_many_advisory(filters, skip, limit):
    """
    根据关键词查找问题
    :param filters
    :param skip
    :param limit
    :return:
    """
    filters["is_answer"] = 1
    cursor = mongodb.query_many(db_name["advisory"], filters=filters, skip=skip, limit=limit)
    return cursor


def find_one_advisory(filters=None):
    """
    根据标题查找问题
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["advisory"], filters)
    return resource


def update_one_blog(filter, doc):
    """
    记录问题查询次数
    :param filter:
    :return:

    """
    mongodb.update_one(db_name["blog"], filter, doc)


def find_one_pluralism(filters=None):
    """
    根据标题查找问题
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["pluralism"], filters)
    return resource


def insert_one_pluralism(doc=None):
    """
    添加简历
    :param doc:
    :return:
    """
    doc["upload_time"] = datetime.datetime.now()
    return mongodb.insert_one(db_name["pluralism"], doc)


def find_one_access(filters=None):
    """
    根据ip查找访问记录
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["access"], filters)
    return resource


def insert_one_access(doc=None):
    """
    添加访问记录
    :param doc:
    :return:
    """
    now_time = datetime.datetime.now()
    doc["upload_time"] = now_time
    doc["access_record"] = [int(time.time())]
    doc["access_num"] = 1
    return mongodb.insert_one(db_name["access"], doc)


def find_one_spider(filters=None):
    """
    根据ip查找机器人记录
    :param username:
    :return:
    """
    resource = mongodb.query_one(db_name["spider"], filters)
    return resource


def update_one_spider(filter, doc):
    """
    更新机器人记录
    :param filter:
    :return:

    """
    mongodb.update_one(db_name["spider"], filter, doc)


def insert_one_spider(doc=None):
    """
    添加访问记录
    :param doc:
    :return:
    """
    doc["lock_record"] = 1
    return mongodb.insert_one(db_name["spider"], doc)


def update_one_access(filter, doc):
    """
    更新访问记录
    :param filter:
    :return:

    """
    doc["access_num"] += 1
    mongodb.update_one(db_name["access"], filter, doc)


def delete_one_spider(filters):
    """
    删除封锁记录记录
    :param filters:
    :return:
    """
    return mongodb.delete_one(db_name["spider"], filters)
