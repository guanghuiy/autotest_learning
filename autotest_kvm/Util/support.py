import logging
import os

import yaml

from Data import common_api

logger = logging.getLogger('AutoTest_Api')


def read_yaml(file_name):
    """
    读取yaml文件
    """
    yaml_file = os.path.join(common_api.YAML_PATH, '%s.yaml' % file_name)
    if os.path.exists(yaml_file):
        logger.info("Start to read yaml file : %s.yaml", file_name)
        f = open(yaml_file, "r", encoding="utf-8")
        cfg = yaml.safe_load(f.read())
        logger.info("Had read the info")
        return cfg
    else:
        logger.error("The file: %s is not exist", file_name)
        raise FileNotFoundError('please check the file path')


