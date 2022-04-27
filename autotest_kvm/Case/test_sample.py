def test_kwargs(**kwargs):
    """
    当参数中需要传入关键字使用 **kwargs
    :param kwargs:
    :return:
    """
    if kwargs is not None:
        for key in kwargs:
            print("{} = {}".format(key, kwargs[key]))


def test_args(*args):
    """
    当不确定需要多少个参数时使用 *args
    :param args:
    :return:
    """
    if args is not None:
        for arg in args:
            print("输入数据为：" + arg)


if __name__ == "__main__":
    # test_kwargs(name="python", value="6")
    test_args("python", "1", "6")
