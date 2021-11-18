# CONF

name = "lib_detect_testenv"
title = "detects if pytest or doctest or pyrunner on pycharm is running"
version = "v1.0.0"
url = "https://github.com/bitranox/lib_detect_testenv"
author = "Robert Nowotny"
author_email = "bitranox@gmail.com"
shell_command = "lib_detect_testenv"


def print_info() -> None:
    print(
        """\

Info for lib_detect_testenv:

    detects if pytest or doctest or pyrunner on pycharm is running

    Version : v1.0.0
    Url     : https://github.com/bitranox/lib_detect_testenv
    Author  : Robert Nowotny
    Email   : bitranox@gmail.com"""
    )