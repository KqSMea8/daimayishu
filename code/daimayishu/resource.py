# coding=utf-8
"""
资源处理模块
"""
from flask import (
    Blueprint, flash, render_template, request, current_app
)
import re
import sys
from backend import mongodb_utils
from common import oss_utils, oppose_rebot

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("resource", __name__, url_prefix="/resource")

global_resource = None
page_obj = None


@bp.route("/index", methods=("GET",))
def index():
    """
    查询资源（按时间倒序）
    :return:
    """

    global global_resource
    global page_obj
    try:
        key_word = request.args.get("key_word", None)
        page_index = int(request.args.get("page_index", 1))
        page_num = int(request.args.get("page_num", 11))
        if page_num <= 0 or page_index <= 0:
            flash("参数异常")
            return render_template("resource/index.html")
        skip = (page_index - 1) * (page_num - 1)
        limit = page_num
        filter = None
        if key_word and key_word != "":
            rex = re.compile('.*' + key_word + '.*', re.IGNORECASE)
            filter = {"title": rex}
        cursor = mongodb_utils.find_many_resource(filters=filter, skip=skip, limit=limit)
        resource = list(cursor)
        global_resource = resource
        page_obj = {"page_index": page_index, "page_prev": page_index - 1, "page_next": page_index + 1,
                    "key_word": key_word if key_word else None, "has_prev": True if page_index > 1 else None,
                    "has_next": True if len(resource) == page_num else None}
        if resource:
            resource = resource[:-1] if len(resource) == page_num else resource
            return render_template("resource/index.html", resource=resource, page_obj=page_obj)
        else:
            flash("暂未收录你所搜索的资源")
            return render_template("resource/index.html")
    except Exception as err:
        flash("系统异常")
        current_app.logger.error(err.message)
        return render_template("resource/index.html")


@bp.route("/download", methods=("GET",))
def download():
    """
    获取资源下载链接
    :return:
    """
    key_word = request.args.get("key_word", None)
    is_rebot, status = oppose_rebot.check_robot_identity(request, "resource/index")
    if is_rebot:
        flash("下载资源配額已达上限或者被识别为有入侵主机的企图导致没有访问权限")
        return render_template("resource/index.html")
    else:
        if status == 2:
            flash("访问资源过于频繁，请1小时后再访问")
            return render_template("resource/index.html")
        if status == 3:
            flash("下载资源配額已达上限，请1小时后再访问，建议你先享受下载好的书籍")
            return render_template("resource/index.html")
    if key_word is None:
        return "找不到资源", 404

    filters = {"title": key_word}
    resource = mongodb_utils.find_one_resource(filters)
    if resource:
        try:
            download_num = resource.get("download_num", 0)
            download_num += 1
            mongodb_utils.update_one_resource(filters, {"download_num": download_num})
            # 向阿里云获取链接
            resource_url = oss_utils.get_url(key_word)
            if resource_url is None:
                raise Exception()
            else:
                flash("下载链接两分钟后将失效，请尽快下载！")
                return render_template("resource/index.html", resource_url=(resource_url,), resource=global_resource,
                                       page_obj=page_obj)
        except Exception:
            flash("读取下载链接异常")
            return render_template("resource/index.html")
    else:
        flash("资源不存在")
        return render_template("resource/index.html")
