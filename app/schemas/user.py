"""
@Time    : 2024/2/5 5:01 PM
@Author  : lan
@DESC    : 
"""
from typing import Optional, Annotated

from pydantic import BaseModel, constr, AfterValidator


class ParamsError(ValueError):
    pass


def validate_username_or_password(value: str):
    value_stripped = value.strip()
    value_length = len(value_stripped)

    if not value_stripped:
        raise ValueError("用户名或密码不能为空")
    elif value_length < 5:
        raise ValueError("用户名或密码不能少于 5 位")
    elif value_length > 20:
        raise ValueError("用户名或密码不能超过 20 位")
    return value_stripped


class UserInfoSchema(BaseModel):
    id: int
    nickname: Optional[constr(max_length=10)] = "momo"
    email: Optional[constr(max_length=30)] = None
    phone: Optional[constr(max_length=15)] = None
    avatar: Optional[str] = None
    role: int = 1


class UserLoginSchema(BaseModel):
    username: Annotated[str, AfterValidator(validate_username_or_password)]
    password: Annotated[str, AfterValidator(validate_username_or_password)]


class UserRegisterSchema(UserInfoSchema, UserLoginSchema):
    id: int = None
    role: int = None
