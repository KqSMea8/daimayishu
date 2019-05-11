# coding=utf-8

"""
微信公众号平台
"""

from flask import (
    Blueprint, flash, render_template, request, current_app

)
import sys
import json
import time
import requests
import xmltodict

from backend import mongodb_utils

reload(sys)

sys.setdefaultencoding('utf8')

bp = Blueprint("weixin", __name__, url_prefix="/weixin")

WEIXIN_SERVER = "https://api.weixin.qq.com/"
TOKEN_PATH = "cgi-bin/token"
CREATE_MENU_PATH = "menu/create"
APPID = "wx5db0ba37ed754be2"
SECRET = "c2795a37d70cbcc4793d422023b68f76"
ACCESS_TOKEN_DICT = None


@bp.route("/entry", methods=("GET", "POST"))
def index():
    """
    打开关于我页面
    :return:
    """
    if request.method == "GET":
        echostr = request.args.get("echostr")
        return echostr
    else:
        xml_str = request.data
        if not xml_str:
            return 500
        xml_dict = xmltodict.parse(xml_str)
        xml_dict = xml_dict.get("xml")
        msg_type = xml_dict.get("MsgType")
        resp_dict = None
        print(msg_type)
        if msg_type == "text":
            # 用户发送文本消息
            resp_dict = make_text_response_xml(xml_dict, xml_dict.get("Content"))
        elif msg_type == "event":
            if xml_dict.get("Event") == "subscribe":
                # 用户关注事件
                resp_dict = make_text_response_xml(xml_dict, "欢迎来到代码艺术")
            elif xml_dict.get("Event") == "CLICK":
                if xml_dict.get("EventKey") == "blog":
                    # 用户点击博客菜单
                    resp_dict = make_text_response_xml(xml_dict, "博客")
        if resp_dict is None:
            resp_dict = make_text_response_xml(xml_dict, "暂不支持此类型的消息对话")
        resp_xml_str = xmltodict.unparse(resp_dict)
        return resp_xml_str


def make_text_response_xml(xml_dict, content):
    """
    构建返回格式文本格式的xml
    :return:
    """
    resp_dict = {
        "xml": {
            "ToUserName": xml_dict.get("FromUserName"),
            "FromUserName": xml_dict.get("ToUserName"),
            "CreateTime": int(time.time()),
            "MsgType": "text",
            "Content": content
        }
    }
    return resp_dict


def create_menu():
    """
    创建自定义菜单
    """
    if ACCESS_TOKEN_DICT is None:
        get_access_token()
    else:
        if int(time.time()) > ACCESS_TOKEN_DICT["expires_time"]:
            # 过期了
            get_access_token()
    try:
        request_path = "{0}{1}?access_token={2}".format(WEIXIN_SERVER, CREATE_MENU_PATH,
                                                        ACCESS_TOKEN_DICT["access_token"])
        menu_json = {
            "button": [
                {
                    "type": "click",
                    "name": "博客",
                    "key": "blog"
                },
                {
                    "type": "click",
                    "name": "问题",
                    "key": "advisory"
                }
            ]
        }
        print request_path
        headers = {'Content-Type': 'application/json'}
        response = requests.post(request_path, headers=headers, data=json.dumps(menu_json))
        print(response)
        print("创建成功")
    except Exception as err:
        print("创建失败,{0}".format(err.message))


def get_access_token():
    """
    获取access_token
    :return:
    """
    global ACCESS_TOKEN_DICT
    try:
        request_path = WEIXIN_SERVER + TOKEN_PATH
        response = requests.get(request_path,
                                params={"grant_type": "client_credential", "appid": APPID, "secret": SECRET})
        content = json.loads(response.text)
        ACCESS_TOKEN_DICT = content
        ACCESS_TOKEN_DICT["expires_time"] = int(time.time()) + 7000
        print("读取access_token正常，{0}".format(ACCESS_TOKEN_DICT["access_token"]))
    except Exception as err:
        print ("读取access_token异常，{0}".format(err.message))


if __name__ == "__main__":
    create_menu()
