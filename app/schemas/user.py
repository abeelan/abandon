"""
@Time    : 2024/2/5 5:01 PM
@Author  : lan
@DESC    : 
"""
from typing import Optional

from pydantic import BaseModel, constr, field_validator


class ParamsError(ValueError):
    pass


class UserInfoSchema(BaseModel):
    id: int
    nickname: Optional[constr(max_length=10)] = "momo"
    email: Optional[constr(max_length=30)] = None
    phone: Optional[constr(max_length=15)] = None
    avatar: Optional[str] = None
    role: int


class UserLoginSchema(BaseModel):
    username: constr(max_length=20)
    password: constr(max_length=20)

    @classmethod
    @field_validator("username", "password")
    def not_empty(cls, value: str) -> str:
        # TODO: 为空校验，返回到接口的异常信息里面，不知道为啥不生效！？
        # https://docs.pydantic.dev/latest/concepts/validators/
        if len(value.strip()) == 0:
            raise ValueError("用户名或密码不能为空")
        return value


class UserRegisterSchema(UserInfoSchema, UserLoginSchema):
    id: int = None
    role: int = None
