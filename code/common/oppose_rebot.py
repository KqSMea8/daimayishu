# coding=utf-8

"""
反爬虫模块
"""
import time
from backend import mongodb_utils
import datetime

ONE_HOUR = 60 * 60
ONE_DAY = 60 * 60 * 24
ONE_MIN = 60


def check_forever_spider(spider_record, ua, ua_record, access_record, access_filters, access_num):
    """
    检测是否是永久封锁的爬虫，被封锁十次以上可认为是永久封锁
    :param spider_record:
    :param ua:
    :param ua_record:
    :param access_record:
    :param access_filters:
    :return:
    """
    if spider_record["lock_record"] > 10:
        update_access_record(access_filters, access_record, ua, ua_record, access_num)
        return True
    return False


def update_access_record(access_filters, access_record, ua, ua_record, access_num):
    """
    更新访问记录
    :param access_filters:
    :param access_record:
    :param ua:
    :param ua_record:
    :return:
    """
    if ua not in ua_record:
        ua_record.append(ua)
    if len(ua_record) == 6:
        ua_record.remove(ua_record[0])
    access_record.append(int(time.time()))  # 仅记录最近5此的访问记录
    if len(access_record) == 6:
        access_record.remove(access_record[0])
    access_doc = {
        "access_record": access_record,
        "ua_record": ua_record,
        "access_num": int(access_num)
    }
    mongodb_utils.update_one_access(access_filters, access_doc)


def insert_access_record(access_filters, ua):
    """
    新增访问记录
    :param access_filters:
    :param ua:
    :return:
    """
    access_filters["ua_record"] = [ua]
    mongodb_utils.insert_one_access(access_filters)


def update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record):
    """
    更新爬虫机器人记录
    :param lock_time:
    :param release_time:
    :param remote_addr:
    :param spider_filters:
    :param spider_record:
    :return:
    """
    if spider_record:
        spider_doc = {"lock_record": spider_record["lock_record"] + 1,
                      "lock_time": lock_time,
                      "release_time": release_time}
        mongodb_utils.update_one_spider(spider_filters, spider_doc)
    else:
        spider_doc = {"lock_time": lock_time,
                      "release_time": release_time,
                      "remote_addr": remote_addr}
        mongodb_utils.insert_one_spider(spider_doc)


def check_robot_identity(request, request_path):
    """
    测验机器人身份
    1 ua 为空或者ua是常用爬虫的拒绝,封一天，其他的封一小时
    2 referer 必须是本站来的
    3 记录remote host访问频率 快的拒绝 规律的拒绝
    :param request:
    :param request_path:
    :return:
    1表示确认是机器人
    0表示不确定是机器人
    2表示获取资源太快
    3表示当天获取资源已达上限
    """
    ua = request.headers.get('User-Agent')
    referer_url = request.headers.get("Referer", None)
    remote_addr = request.remote_addr
    host_url = request.host_url
    spider_filters = {"remote_addr": remote_addr}
    spider_record = mongodb_utils.find_one_spider(spider_filters)
    access_filters = {"remote_addr": remote_addr}
    access_obj = mongodb_utils.find_one_access(access_filters)
    request_path = host_url + request_path
    if ua is None or referer_url is None or host_url not in request_path:
        lock_time = int(time.time())
        release_time = lock_time + ONE_DAY
        update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record)
        if access_obj:
            ua_record = access_obj.get("ua_record")
            access_record = access_obj.get("access_record")
            update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
        else:
            insert_access_record(access_filters, ua)
        return True, 1

    if access_obj is None:
        insert_access_record(access_filters, ua)
        return False, 0
    ua_record = access_obj.get("ua_record")
    access_record = access_obj.get("access_record")
    if spider_record:
        # forever_spider = check_forever_spider(spider_record, ua, ua_record, access_record, access_filters,
        #                                       access_obj["access_num"])
        # if forever_spider:
        #     return True, 1
        release_time_stamp = spider_record["release_time"]
        access_time_stamp = int(time.time())
        if access_time_stamp < release_time_stamp:
            update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
            return True, 1
        else:
            ua_record = []
            access_record = []
            update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
            mongodb_utils.delete_one_spider({"remote_addr": remote_addr})
            return False, 0
    ua_num = len(ua_record) + 1 if ua not in ua_record else len(ua_record)
    if ua_num > 5:
        lock_time = int(time.time())
        release_time = lock_time + ONE_HOUR
        update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record)
        update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
        return True, 1
    else:
        record_num = len(access_record)
        if record_num < 5:
            update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
            return False, 0

        else:
            diff_time = []
            for i in xrange(record_num - 1):
                diff_time.append(access_record[i + 1] - access_record[i])
                # if diff_time[0] * record_num * 0.8 < sum(diff_time) and diff_time[0] * record_num * 1.1 > sum(
                #         diff_time):
                #     lock_time = int(time.time())
                #     release_time = lock_time + 60 * 60 * 24
                #     update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record)
                #     update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
                #     return True
            if sum(diff_time) < 8:
                lock_time = int(time.time())
                release_time = lock_time + ONE_HOUR
                update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record)
                update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
                return False, 2
            if check_quote(access_record) >= 5:
                lock_time = int(time.time())
                release_time = lock_time + ONE_HOUR
                update_spider_record(lock_time, release_time, remote_addr, spider_filters, spider_record)
                update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
                return False, 3
        update_access_record(access_filters, access_record, ua, ua_record, access_obj["access_num"])
        return False,0


def check_quote(access_record):
    """
    检测该用户当日下载资源是否已达上限
    :param access_record:
    :return:
    """
    cur_time = datetime.datetime.now()
    cur_time_str = "{0}-{1}-{2} 00:00:00".format(cur_time.year, cur_time.month, cur_time.day)
    last_time_str = "{0}-{1}-{2} 23:59:59".format(cur_time.year, cur_time.month, cur_time.day)
    cur_time_str = time.strptime(cur_time_str, "%Y-%m-%d %H:%M:%S")
    cur_time_stamp = int(time.mktime(cur_time_str))
    last_time_str = time.strptime(last_time_str, "%Y-%m-%d %H:%M:%S")
    last_time_stamp = int(time.mktime(last_time_str))
    quota = map(lambda x: 1 if x > cur_time_stamp and x < last_time_stamp else 0, access_record)
    quota = sum(quota)
    return quota
