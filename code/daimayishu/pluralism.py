# coding=utf-8
"""
我想兼职模块
"""

from flask import (
    Blueprint, flash, redirect, render_template, request, url_for, current_app
)
import os
import sys
import uuid
from common import file_utils
from backend import mongodb_utils

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("pluralism", __name__, url_prefix="/pluralism")


@bp.route("/index", methods=("GET",))
def index():
    """
    打开我想兼职页面
    :return:
    """
    return render_template("pluralism.html")


@bp.route("/add", methods=("POST",))
def add():
    """
    保存兼职信息
    :return:
    """
    try:
        name = request.form["name"]
        age = request.form["age"]
        identity = request.form["identity"]
        pluralism_type = request.form["pluralismType"]
        freetime = request.form["freetime"]
        contact = request.form["contact"]
        skill = request.form["skill"]
    except Exception:
        flash("参数异常")
        return redirect(url_for("pluralism.index"))
    if 'resume' not in request.files:
        flash('未找到上传文件')
        return redirect(url_for("pluralism.index"))
    file = request.files['resume']
    if file.filename == '':
        flash('上传文件不能为空')
        return redirect(url_for("pluralism.index"))
    if file and file_utils.allowed_file(file.filename):
        file_ext = file_utils.get_file_ext(file.filename)
        filename = "{0}_{1}_{2}_{3}{4}".format(age, name, str(uuid.uuid4()), ".", file_ext)
        try:
            file.save(os.path.join(current_app.config['RESUME_FOLDER'], filename))
        except Exception as err:
            flash("文件读取异常")
            return redirect(url_for("pluralism.index"))
        doc = {
            "name": name,
            "age": age,
            "identity": identity,
            "pluralism_type": pluralism_type,
            "freetime": freetime,
            "contact": contact,
            "skill": skill,
            "resume_path": filename
        }
        mongodb_utils.insert_one_pluralism(doc)
        flash("已收藏你的求职信息，如果有合适你的任务，会有专人联系你，感谢你的投递")
        return redirect(url_for("pluralism.index"))
    else:
        flash("上传的文件被识别为非法文件！")
        return redirect(url_for("pluralism.index"))