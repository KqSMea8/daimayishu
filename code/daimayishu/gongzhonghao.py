# coding=utf-8
"""
公众号模块
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import sys

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("gongzhonghao", __name__, url_prefix="/gongzhonghao")


@bp.route("/index", methods=("GET",))
def index():
    """
    打开公众号页面
    :return:
    """
    return render_template("gongzhonghao.html")
