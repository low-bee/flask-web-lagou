import requests
import json
import re
import logging
import os
from logging.handlers import BaseRotatingHandler


def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


if __name__ == '__main__':
    file_handler = BaseRotatingHandler(filename="./spiderlog", mode="a", encoding="utf-8")
    logging.basicConfig(filename="./spiderlog", format="%(asctime)s-%(levelname)s-%(name)s-%(message)s", level=logging.INFO)

    logging.info("发生了一个错误*")