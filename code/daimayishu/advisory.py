# coding=utf-8
"""
我要咨询模块
"""

from flask import (
    Blueprint, flash, render_template, request
)
import sys
import re

from backend import mongodb_utils

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("advisory", __name__, url_prefix="/advisory")


@bp.route("/index", methods=("GET",))
def index():
    """
    打开我要咨询页面
    :return:
    """
    page = "advisory/index.html"
    try:
        key_word = request.args.get("key_word", None)
        page_index = int(request.args.get("page_index", 1))
        page_num = int(request.args.get("page_num", 11))  # 因为需要判断下一页是否还有数据，因此查询的时候特意多查询一条
        if page_num <= 0 or page_index <= 0:
            flash("参数异常")
            return render_template(page)
        skip = (page_index - 1) * (page_num - 1)  # 因为返回给前端的值去[:-2]条数据
        limit = page_num
        filter = {}
        if key_word and key_word != "":
            question = re.compile('.*' + key_word + '.*', re.IGNORECASE)
            filter = {"question": question}

        cursor = mongodb_utils.find_many_advisory(filters=filter, skip=skip, limit=limit)
        advisories = list(cursor)
        page_obj = {"page_index": page_index, "page_prev": page_index - 1, "page_next": page_index + 1,
                    "has_prev": True if page_index > 1 else None,
                    "has_next": True if len(advisories) == page_num else None,
                    "key_word": key_word if key_word else None, }
        if advisories:
            advisories = advisories[:-1] if len(advisories) == page_num else advisories
            return render_template(page, advisories=advisories, page_obj=page_obj)
        else:
            flash("没有找到类似的问题")
            return render_template(page)
    except Exception:
        flash("系统异常")
        return render_template(page)


@bp.route("/add", methods=("GET", "POST"))
def add():
    """
    提问
    :return:
    """

    page = "/advisory/add.html"
    if request.method == "GET":
        return render_template(page)
    elif request.method == "POST":
        try:
            question = request.form["question"]
            doc = {"question": question}
            if question == "":
                flash("内容不能为空")
                return render_template(page)
            if question:
                result = mongodb_utils.insert_one_advisory(doc)
                if result:
                    flash("问题已提交，本站会在24小时内做出答复，请关注本站或者公众号，获得相应的答案")
                    return render_template(page)
                else:
                    flash("问题已存在")
                    return render_template(page)
            else:
                flash("参数不全")
                return render_template(page)
        except Exception:
            flash("系统异常")
            return render_template(page)

    else:
        return render_template(page)


@bp.route("/show", methods=("GET",))
def show():
    try:
        title = request.args.get("title", None)
        if title:
            filters = {"title": title}
            advisory = mongodb_utils.find_one_blog(filters)
            if advisory:
                doc = {"click_num": advisory.get("click_num", 0) + 1}
                mongodb_utils.update_one_blog(filters, doc)
            template = "/advisory/{0}{1}".format(title, ".html")
            return render_template(template)
        return None, 404
    except Exception:
        return u"找不到资源", 404
