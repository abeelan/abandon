from fastapi import APIRouter, Depends

from app.dao.user import UserDao

# from app.handler.response import Response
from app.schemas.user import UserLoginSchema, UserRegisterSchema
from app.utils.log import log


router = APIRouter(prefix="/user")

dao = UserDao()


@router.get("/info")
async def get_user(uid: int = None, username: str = None):
    try:
        if uid is not None:
            user = await dao.get_user_info(uid)
        elif username is not None:
            user = await dao.get_user_info(username)
        else:
            return {"error": "必须提供 uid 或 username 参数"}
        return {"user": user, "msg": "查找成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}


@router.get("/list")
async def user_list(page: int = 1, limit: int = 10):
    users = await dao.get_user_list(offset=(page - 1) * limit, limit=limit)
    return {"users": users}


@router.post("/register")
async def register(user: UserRegisterSchema):
    try:
        user = await dao.register(user)
        return {"user": user.username, "msg": "注册成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}


@router.post("/login")
async def login(user: UserLoginSchema):
    try:
        user = await dao.login(user)
        return {"user": user, "msg": "登录成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}


@router.post("/reset-password")
async def reset_password(login: UserLoginSchema):
    try:
        user = await dao.reset_password(login)
        return {"user": user.username, "msg": "修改成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}
