import sys

import uvicorn
from loguru import logger
from fastapi import FastAPI

from app.models import db_helper
from app.routers import user
from app.utils.log import log

sys.path.append(__file__)


app = FastAPI()
app.include_router(user.router)


@app.get("/")
async def root():
    log.info("根目录被请求了")
    return {"message": "ok"}


app.add_event_handler("startup", db_helper.init_tables)


if __name__ == "__main__":
    # 命令行运行 切到 poetry 环境
    # python -m uvicorn main:app --reload
    uvicorn.run(app, host="0.0.0.0", reload=False)
