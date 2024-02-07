from datetime import datetime
from sqlalchemy import Column, String, INT, TIMESTAMP, Boolean, BIGINT

from app.models import Base


class User(Base):
    id = Column(INT, primary_key=True)
    username = Column(String(16), unique=True, index=True)
    password = Column(String(32), unique=False)

    nickname = Column(String(16), index=True)
    phone = Column(String(12), unique=True)
    email = Column(String(64), unique=True)
    avatar = Column(String(128), nullable=True, default=None)

    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    deleted_at = Column(BIGINT, nullable=False, default=0)  # 非 0 为删
    update_user = Column(INT, nullable=True)  # 修改人
    last_login_at = Column(TIMESTAMP)

    role = Column(INT, default=0, comment="0: 普通用户 1: 组长 2: 超级管理员")
    # 管理员可以禁用某个用户，当他离职后
    is_valid = Column(Boolean, nullable=False, default=True, comment="是否在职")
