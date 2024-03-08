import sys

import uvicorn
from fastapi import FastAPI

from app.models import db_helper
from app.routers import user
from app.routers import request
from app.utils.log import log
from config import LOGO_STR

sys.path.append(__file__)


app = FastAPI()
app.include_router(user.router)
app.include_router(request.router, prefix="/request", tags=["请求调试"])


@app.get("/")
async def root():
    log.info("根目录被请求了")
    return {"message": "ok"}


app.add_event_handler("startup", db_helper.init_tables)


if __name__ == "__main__":
    log.debug(LOGO_STR)
    # 命令行运行 切到 poetry 环境
    # python -m uvicorn main:app --reload
    uvicorn.run("main:app", host="0.0.0.0", reload=True)
