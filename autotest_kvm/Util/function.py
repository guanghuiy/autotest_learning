import logging

import requests

from Data.common_api import GET_TOKEN_URL

logger = logging.getLogger("AutoTest_KVM_Api")
# conf = support.read_yaml('cloud_os_test')['login']
# user = conf['username']
# psw = conf['password']


def get_token(username, password):
    header = {"username": username, "password": password}
    res = requests.get(GET_TOKEN_URL, headers=header).json()
    logging.info("get_token : %s" % res)
    # print("res", res['Access-Token'])
    return res['Access-Token']

# get_token(user, psw)
