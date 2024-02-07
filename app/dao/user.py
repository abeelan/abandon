"""
user dao
"""
from typing import List
from datetime import datetime
from sqlalchemy.future import select
from sqlalchemy import update, or_, and_

from app.middleware.auth import JWTAuth
from app.utils.log import log
from app.models import async_session
from app.models.user import User
from app.dao import BaseDao

from app.schemas.user import UserLoginSchema, UserRegisterSchema, UserInfoSchema


class UserDao(BaseDao):
    model = User
    jwt = JWTAuth()

    async def get_user_list(self, offset=0, limit=10) -> List:
        query = select(self.model).offset(offset).limit(limit)
        return await self.read(query)

    async def get_user_info(self, arg) -> dict:
        if isinstance(arg, int):
            query = select(self.model).where(self.model.id == arg)
        elif isinstance(arg, str):
            query = select(self.model).where(self.model.username == arg)
        else:
            raise Exception("请输入 id 或 username 进行查询。")

        result = await self.read(query)
        if len(result) == 0:
            raise Exception("用户不存在")

        user = UserInfoSchema(**result[0].__dict__)
        return user.dict()

    async def user_exists(self, username) -> bool:
        users = await self.get_user_info(username)
        if len(users) != 0:
            return True
        else:
            return False

    async def register(self, register: UserRegisterSchema):
        # 已注册用户判断
        if await self.user_exists(register.username):
            raise Exception("用户名已注册")

        new_user = User(**register.dict())
        new_user.password = (self.jwt.add_salt(register.password),)
        new_user.last_login_at = datetime.now()

        await self.create(new_user)
        return register

    async def login(self, login: UserLoginSchema) -> dict:
        pwd = self.jwt.add_salt(login.password)
        condition = and_(
            self.model.username == login.username,
            self.model.password == pwd,
            self.model.deleted_at == 0
        )

        query = select(self.model).where(condition)
        result_list = await self.read(query)
        if len(result_list) == 0:
            raise Exception("用户名或密码错误")
        user = result_list[0]
        if not user.is_valid:
            raise Exception("您的账号已被封禁, 请联系管理员")

        sql = update(User).where(condition).values(last_login_at=datetime.now())
        await self.update(sql)

        user_info = UserInfoSchema(**user.__dict__)
        return user_info.dict()

    async def reset_password(self, login: UserLoginSchema):
        if await self.user_exists(login.username) is False:
            raise Exception("用户名暂未注册")

        pwd = self.jwt.add_salt(login.password)
        sql = (
            update(User)
            .where(self.model.username == login.username)
            .values(password=pwd)
        )

        await self.execute_begin(sql, "重置密码失败")
        return login
