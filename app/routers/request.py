"""
@Time    : 2024/3/5 18:14
@Author  : lan
@DESC    : 
"""

from fastapi import APIRouter
from pydantic import BaseModel, validator

from app.handler.response import Response
from app.middleware.http_client import Request
from app.middleware.http_client_async import async_get


router = APIRouter()


@router.get("/http")
async def http_request(url):
    try:
        code, resp = await async_get(url)
        if code == 200:
            return Response.success(resp)
        else:
            return Response.failed(f"状态码为{code}，请求失败。", data=resp)
    except Exception as e:
        return Response.failed(e)
