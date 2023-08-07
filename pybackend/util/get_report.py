import os
import json
from loguru import logger


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.mkdir(path)
        logger.debug("---新建文件夹---")
    else:
        logger.debug("---文件夹已存在---")


def mk_json(data, filename):
    try:
        with open(filename, mode='w', encoding='utf-8') as f:
            f.write(data)
    except:
        raise
        # return "发生错误"
    return "写入成功"


def get_report_list(dir_path):
    res = os.listdir(dir_path)
    return res


def read_report(filename):
    try:
        with open(filename, 'r', -1, 'utf-8') as f:
            return f.read()
    except:
        return '文件不存在'
