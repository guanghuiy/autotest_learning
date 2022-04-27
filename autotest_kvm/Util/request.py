import requests


class Request:
    """
    通用请求工具类
    """
    def __init__(self):
        pass

    def request(self, url, method, headers=None, param=None, content_type='application/json'):
        try:
            if method == 'get':
                result = requests.get(url=url, params=param, headers=headers).json()
                return result
            elif method == 'post':
                if content_type == 'application/json':
                    result = requests.post(url=url, json=param, headers=headers).json()
                    return result
                else:
                    result = requests.post(url=url, data=param, headers=headers).json()
                    return result
            else:
                print("http method not allowed!")

        except Exception as e:
            print("http 请求错误：{0}".format(e))

