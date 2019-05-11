# coding=utf-8

"""
mongodb模块
"""

from pymongo import MongoClient, DESCENDING
import datetime

client = None
db = None


def register_mongo_client(host, port, db_name):
    global client
    global db
    if client is None:
        client = MongoClient(host=host, port=port,connect=False)
    if db_name is None:
        raise Exception("必须传入命名空间参数")
    db = client[db_name]


def switch_db(db_name=None):
    """
    切换Mongo操作命名空间
    :param db_name:
    :return:
    """
    global db
    if client is None:
        raise Exception("没有初始化mongo client")
    if db_name is None:
        raise Exception("必须传入集合名称")
    db = client[db_name]


def query_one(tb_name, filters):
    """
    查询一条数据
    :param tb_name:集合名称
    :param filters:
    :return:
    """
    return db[tb_name].find_one(filters)


def insert_one(tb_name, doc):
    """
    插入一条数据
    :param tb_name:集合名称
    :param doc:
    :return:
    """
    create_time = datetime.datetime.now()
    update_time = datetime.datetime.now()
    doc["create_time"] = create_time
    doc["update_time"] = update_time
    return db[tb_name].insert_one(doc)


def replace_one(tb_name, filters, doc):
    """
    重置一条数据
    :param tb_name:集合名称
    :param filters:
    :param doc:
    :return:
    返回1表示修改成功
    返回0表示修改失败
    """
    update_time = datetime.datetime.now()
    doc["update_time"] = update_time
    result = db[tb_name].replace_one(filters, doc, False)
    return result


def update_one(tb_name, filters, doc):
    """
    更新一条数据
    :param tb_name:集合名称
    :param filters:
    :param doc:
    :return:
    返回1表示修改成功
    返回0表示修改失败
    """
    update_time = datetime.datetime.now()
    doc["update_time"] = update_time

    result = db[tb_name].update_one(filters, {"$set": doc}, False)
    return result


def query_many(tb_name, filters, skip, limit):
    """
    查询多条资源
    :param tb_name: 表名
    :param filters: 过滤条件
    :param skip: 起始数
    :param limit: 最大返回数量
    :return:
    """
    if filters:
        cursor = db[tb_name].find(filter=filters, skip=skip, limit=limit, sort=[("create_time", DESCENDING)])
    else:
        cursor = db[tb_name].find(skip=skip, limit=limit, sort=[("create_time", DESCENDING)])
    return cursor


def query_all(tb_name):
    """
    查询全部资源
    :param tb_name: 表名
    :return:
    """
    cursor = db[tb_name].find()
    return cursor


def delete_one(tb_name, fitlers):
    """
    删除指定资源
    :param tb_name: 表名
    :return:
    """
    cursor = db[tb_name].delete_one(fitlers)
    return cursor
