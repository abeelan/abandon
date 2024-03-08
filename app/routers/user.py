from fastapi import APIRouter, Query

from app.dao.user import UserDao
from app.schemas.user import UserLoginSchema, UserRegisterSchema


router = APIRouter(prefix="/user", tags=["用户相关"])

dao = UserDao()


@router.get(
    "/",
    summary="根据 uid 或 username 获取单个用户信息，当两个参数都为空时，返回用户列表数据"
)
async def get_user(
        uid: int = Query(None, description="User ID", gt=0),
        username: str = Query(None, description="Username"),
        page: int = Query(1, gt=0, description="页码"),
        limit: int = Query(10, gt=0, le=100, description="每页记录数")
):
    if uid is not None:
        user = await dao.get_user_info(uid)
    elif username is not None:
        user = await dao.get_user_info(username)
    else:
        offset = (page - 1) * limit
        users = await dao.get_user_list(offset=offset, limit=limit)
        return {"users": users, "message": "查找成功"}
    return {"user": user, "message": "查找成功"}


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
        user.validate()

        user = await dao.login(user)
        return {"user": user, "msg": "登录成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}


@router.post("/reset-password")
async def reset_password(user: UserLoginSchema):
    try:
        user = await dao.reset_password(user)
        return {"user": user.username, "msg": "修改成功"}
    except Exception as e:
        return {"success": False, "msg": str(e)}
