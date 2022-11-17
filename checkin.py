# -*- coding: utf-8 -*-
# @Date    : 2021-04-24 16:31:25
# @Author  : gwentmaster(gwentmaster@vivaldi.net)
# I regret in my life


import json
import logging
import logging.config
import os
import re
import time
from hashlib import md5
from traceback import format_exc
from typing import List

import httpx


USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    + "(KHTML, like Gecko) Chrome/90.0.4430.95 Safari/537.36"
)


def purefast_checkin() -> None:
    """purefast签到
    """

    logger = logging.getLogger("purefast")
    client = httpx.Client(headers={"User-Agent": USER_AGENT})

    email = os.environ["PUREFAST_USER"]
    password = os.environ["PUREFAST_PASSWORD"]

    login_resp = client.post(
        url="https://purefast.net/auth/login",
        data={
            "code": "",
            "email": email,
            "passwd": password,
        }
    )
    logger.info(login_resp.json()["msg"])

    checkin_resp = client.post("https://purefast.net/user/checkin")
    logger.info(checkin_resp.json()["msg"])


if __name__ == "__main__":

    logging.config.dictConfig({
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "logging.Formatter",
                "fmt": (
                    "[%(asctime)s]-[%(name)s]-[%(levelname)s]: %(message)s\n"
                ),
                "datefmt": "%m-%d %H:%M:%S"
            }
        },
        "handlers": {
            "default": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "": {"handlers": ["default"], "level": "INFO"},
        }
    })

    errors = []  # type: List[Exception]
    for func in [
        purefast_checkin
    ]:
        try:
            func()
        except Exception as e:
            errors.append(e)

    if errors:
        print("============ errors ============")
    for er in errors:
        try:
            raise er
        except Exception:
            print(f"--------------------------\n\n{format_exc()}")
