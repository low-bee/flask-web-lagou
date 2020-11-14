class MyError(object):

    @staticmethod
    def ifNotStr():
        raise RuntimeError(
            "username请使用字符串"
        )