# coding=utf-8
"""
我想要模块
"""

from flask import (
    Blueprint, flash, render_template, request
)
import sys

from backend import mongodb_utils

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("want", __name__, url_prefix="/want")


@bp.route("/index", methods=("GET", "POST"))
def index():
    """
    打开关于我页面
    :return:
    """
    page = "/want/index.html"
    if request.method == "GET":
        return render_template(page)
    else:
        wantPdf = request.form["wantPdf"];
        weixinId = request.form["weixinId"]
        wantPdf = wantPdf.split(";")
        if len(wantPdf):
            flash("你要的书太多啦！")
            return render_template(page)
        is_exit_pdf = check_pdf_is_exit(wantPdf)
        if is_exit_pdf:
            flash("部分书籍已收录，请移步到下载书籍资源板块查看！")
            return render_template(page)
        is_follow_user = check_is_follow_user(weixinId)
        if is_follow_user:
            pass
        else:
            flash("请先关注公众号哦，否则无法向你汇报结果。")
            return render_template(page)

def check_pdf_is_exit(wantPdf):
    """
    检查资源是否存在
    :param wantPdf:
    :return:
    """
    for title in wantPdf:
        resource = mongodb_utils.find_one_resource({"title": title})
        if resource:
            return True

def check_is_follow_user(weixinId):
    """
    检查该用户是否关注公众号
    :param weixinId:
    :return:
    """
    return False