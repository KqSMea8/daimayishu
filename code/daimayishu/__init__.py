# coding=utf-8
"""
代码艺术后端管理
"""

import os
from flask import Flask, render_template
import logging
from common import mongodb
import resource, about, service, blog, want, gongzhonghao, advisory, pluralism, weixin


def create_app(test_config=None):
    # 创建和配置app实例
    app = Flask(__name__, instance_relative_config=True)
    # SECRET_KEY是给session加密使用的
    app.config.from_mapping(SECRET_KEY='dev')
    if test_config is None:
        # 加载默认配置
        app.config.from_pyfile('config.py')
    else:
        # 加载用户配置
        app.config.from_mapping(test_config)

    # 创建app路径
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 注册数据库对象
    mongodb.register_mongo_client(app.config.get("TEST_MONGO_HOST"),
                                  app.config.get("TEST_MONGO_PORT"),
                                  app.config.get("TEST_MONGO_DATABASE"))

    # 注册资源蓝图
    app.register_blueprint(resource.bp)
    app.register_blueprint(about.bp)
    app.register_blueprint(service.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(want.bp)
    app.register_blueprint(gongzhonghao.bp)
    app.register_blueprint(advisory.bp)
    app.register_blueprint(pluralism.bp)
    app.register_blueprint(weixin.bp)

    # 根页面
    @app.route('/')
    def index():
        return render_template("about.html")

    # 根页面
    @app.route('/siliaowo')
    def siliaowo():
        return "带上你的需求来哦，加QQ502250351详聊，技术和服务都没得说。我绝对不是骗子，所以你也不要耍滑头。诚信交易！"

    handler = logging.FileHandler('/var/log/daimayishu.log')
    app.logger.addHandler(handler)
    return app


app = create_app()
