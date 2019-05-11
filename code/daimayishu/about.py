# coding=utf-8
"""
关于我模块
"""

from flask import (
    Blueprint, render_template
)
import sys

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("about", __name__, url_prefix="/about")

@bp.route("/index", methods=("GET",))
def index():
    """
    打开关于我页面
    :return:
    """
    return render_template("about.html")