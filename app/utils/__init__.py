"""
@Time    : 2024/2/5 2:47 PM
@Author  : lan
@DESC    :
"""

import os


def get_workdir():
    current_path = os.getcwd()  # 获取当前工作目录

    while current_path != "/":  # 在根目录之前一直循环
        abandon_path = os.path.join(current_path, "abandon")
        if os.path.exists(abandon_path) and os.path.isdir(abandon_path):
            return os.path.abspath(abandon_path)
        current_path = os.path.dirname(current_path)  # 获取当前目录的父目录

    return None  # 如果未找到 abandon 目录，则返回 None
