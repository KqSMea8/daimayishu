# coding=utf-8

"""
文件处理助手
"""

import config


def allowed_file(filename):
    """
    检查文件拓展名
    :param filename:
    :return:
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

def get_file_ext(filename):
    """
    获取文件拓展名
    :param filename:
    :return:
    """
    return filename.rsplit('.', 1)[1].lower()
