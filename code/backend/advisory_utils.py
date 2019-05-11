# coding=utf-8

"""
我要咨询管理端
"""

import config
from common import mongodb
import mongodb_utils
import sys

reload(sys)

sys.setdefaultencoding('utf8')

mongodb.register_mongo_client(config.TEST_MONGO_HOST,
                              int(config.TEST_MONGO_PORT),
                              config.TEST_MONGO_DATABASE)

question_path = "/root/advisory/question"


def get_not_answer_question():
    """
    获取待回答的问题
    :return:
    """
    questions = mongodb_utils.find_not_answer_advisory()
    if questions.count == 0:
        print "沒有问题"
    else:
        with open(question_path, "w") as f_obj:
            for question in questions:
                content = "问题:{0}----文件名:{1}".format(question["question"], question["title"])
                print(content)
                f_obj.writelines(content + "\n")


def set_question_answer():
    """
    将问题标志为已回答
    :return:
    """

    with open(question_path, "r") as f_obj:
        content = f_obj.readline()
        while content:
            title = content.split(":")[-1][:-1] #因为输出的时候，每一行都加了换行符，所以必须去掉
            filters = {"title": title}
            doc = {"is_answer": 1}
            mongodb_utils.update_one_advisory(filters, doc)
            content = f_obj.readline()

    print("更新完成")


if __name__ == "__main__":
    # 查詢待回答問題
    # get_not_answer_question()

    # 将待回答问题更新为已回答
     set_question_answer()
