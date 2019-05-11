# coding=utf-8
"""
博客模块
"""

from flask import (
    Blueprint, flash, render_template, request
)
import sys
import re

reload(sys)

sys.setdefaultencoding('utf8')
from backend import mongodb_utils

bp = Blueprint("blog", __name__, url_prefix="/blog")


@bp.route("/index", methods=("GET",))
def index():
    """
    打开博客列表
    :return:
    """
    try:
        category = request.args.get("category", None)
        key_word = request.args.get("key_word", None)
        page_index = int(request.args.get("page_index", 1))
        page_num = int(request.args.get("page_num", 11))  # 因为需要判断下一页是否还有数据，因此查询的时候特意多查询一条
        if page_num <= 0 or page_index <= 0:
            flash("参数异常")
            return render_template("blog/index.html")
        skip = (page_index - 1) * (page_num - 1)  # 因为返回给前端的值去[:-2]条数据
        limit = page_num
        filter = None
        if key_word and key_word != "":
            title = re.compile('.*' + key_word + '.*', re.IGNORECASE)
            filter = {"title": title}
        if category and category != "":
            filter = {"category": category}

        cursor = mongodb_utils.find_many_blog(filters=filter, skip=skip, limit=limit)
        blogs = list(cursor)
        page_obj = {"page_index": page_index, "page_prev": page_index - 1, "page_next": page_index + 1,
                    "category": category if category else None, "has_prev": True if page_index > 1 else None,
                    "has_next": True if len(blogs) == page_num else None, "key_word": key_word if key_word else None, }
        category_info = get_category_info()
        if blogs:
            blogs = blogs[:-1] if len(blogs) == page_num else blogs
            return render_template("/blog/index.html", blogs=blogs, page_obj=page_obj, category_info=category_info)
        else:
            flash("没有找到相关博客")
            return render_template("/blog/index.html", category_info=category_info)
    except Exception:
        flash("系统异常")
        return render_template("/blog/index.html")


@bp.route("/show", methods=("GET",))
def show():
    try:
        title = request.args.get("title", None)
        if title:
            filters = {"title": title}
            blog = mongodb_utils.find_one_blog(filters)
            if blog:
                doc = {"click_num": blog.get("click_num", 0) + 1}
                mongodb_utils.update_one_blog(filters, doc)
            template = "/blog/{0}{1}".format(title, ".html")
            return render_template(template)
        return None, 404
    except Exception:
        return u"找不到资源", 404


def get_category_info():
    """
    统计每种类目有多少文章
    :return:
    """
    cursor = mongodb_utils.find_all_blog()
    category_info = [item["category"] for item in cursor]
    category_set = set(category_info)
    return [{"name": category, "num": category_info.count(category)} for category in category_set]
