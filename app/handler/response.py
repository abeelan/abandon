"""
@Time    : 2024/2/5 5:11 PM
@Author  : lan
@DESC    :
"""

import os
from datetime import datetime
from decimal import Decimal
from typing import Any

from starlette.background import BackgroundTask
from starlette.responses import FileResponse

from app.handler.encoder import jsonable_encoder
from app.models.user import User


class Response:
    """响应数据格式化封装"""

    @classmethod
    def model_to_dict(cls, obj, *ignore: str) -> dict:
        """将表模型转为字典"""
        if getattr(obj, "__tablename__", None) is None:
            # 非数据库表模型数据
            return obj

        data = dict()
        for c in obj.__table__.columns:
            if c.name in ignore:
                continue
            value = getattr(obj, c.name)

            if isinstance(value, datetime):
                data[c.name] = value.strftime("%Y-%m-%d %H:%M:%S")
            else:
                data[c.name] = value
        return data

    @classmethod
    def model_to_list(cls, arr: list, *ignore: str):
        """将列表中的表模型逐个转为字典"""
        return [Response.model_to_dict(x, *ignore) for x in arr]

    @classmethod
    def model_to_dict_recursive(cls, obj) -> dict:
        """字典嵌套表模型递归解析为字典"""
        for k, v in obj.items():
            if isinstance(v, dict):
                cls.model_to_dict_recursive(v)
            elif isinstance(v, list):
                obj[k] = cls.model_to_list(v)
            else:
                obj[k] = cls.model_to_dict(v)
        return obj

    @classmethod
    def json_serialize(cls, obj) -> dict:
        """自定义解码类型，将 sql 类型转为 json 字符串"""
        ans = dict()
        for k, o in dict(obj).items():
            if isinstance(o, set):
                ans[k] = list(o)
            elif isinstance(o, datetime):
                ans[k] = o.strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(o, Decimal):
                ans[k] = str(o)
            elif isinstance(o, bytes):
                ans[k] = o.decode(encoding="utf-8")
            else:
                ans[k] = o
        return ans

    @classmethod
    def parse_sql_result(cls, arr: list):
        columns = []
        if len(arr) > 0:
            columns = list(arr[0].keys())
        return columns, [cls.json_serialize(obj) for obj in arr]

    @classmethod
    def encode_json(cls, data: Any, *exclude: str):
        return jsonable_encoder(
            data,
            exclude=exclude,
            custom_encoder={datetime: lambda x: x.strftime("%Y-%m-%d %H:%M:%S")},
        )

    @classmethod
    def base_resp(cls, code: int, msg: str, data):
        if data is None:
            data = []
        return {"code": code, "message": msg, "data": data}

    @classmethod
    def success(cls, data=None, code=0, msg="操作成功", exclude=()):
        return cls.encode_json(dict(code=code, msg=msg, data=data), *exclude)

    @classmethod
    def records(cls, data: list, code=0, msg="操作成功"):
        return dict(code=code, msg=msg, data=cls.model_to_list(data))

    @classmethod
    def success_with_size(cls, data=None, code=0, msg="操作成功", total=0):
        if data is None:
            return cls.encode_json(dict(code=code, msg=msg, data=list(), total=0))
        return cls.encode_json(dict(code=code, msg=msg, data=data, total=total))

    @classmethod
    def failed(cls, msg, code=110, data=None):
        return dict(code=code, msg=str(msg), data=data)

    @staticmethod
    def forbidden():
        return dict(code=403, msg="对不起, 你没有权限")

    @classmethod
    def file(cls, filepath, filename):
        return FileResponse(
            filepath,
            filename=filename,
            background=BackgroundTask(lambda: os.remove(filepath)),
        )


if __name__ == "__main__":
    resp = Response()

    user = User(username="123", password="pwd", nickname="nickname", email="email")
    print(resp.model_to_dict(user))
    print(Response.model_to_dict(user))

    users = [user, user]
    print(resp.model_to_list(users))

    user_dict = {"user": user, "users": {"users1": users}}
    print(resp.model_to_dict_recursive(user_dict))

    test_data = [
        {"id": 1, "name": "John", "age": 25},
        {"id": 2, "name": "Alice", "age": 30},
        {"id": 3, "name": "Bob", "age": 28},
    ]
    a, b = resp.parse_sql_result(test_data)
    print(a)  # ['id', 'name', 'age']
    print(b)  # 将 sql 数据类型转换后的 dict
