"""
@Time    : 2024/2/6 14:44
@Author  : lan
@DESC    : 
"""

from config import settings


assert settings.MYSQL.HOST == "127.0.0.1"
assert settings.MYSQL.USERNAME == "root"
assert settings.MYSQL.DATABASE == "abandon"
