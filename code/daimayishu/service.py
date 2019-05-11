# coding=utf-8
"""
服务模块
"""

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
import sys

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("service", __name__, url_prefix="/service")


@bp.route("/index", methods=("GET",))
def index():
    """
    打开服务页面
    :return:
    """
    return render_template("/service/index.html")
