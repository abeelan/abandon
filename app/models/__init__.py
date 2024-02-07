"""
数据库初始化: 建库 & API & 定义表结构
"""
from copy import deepcopy
from enum import Enum
from typing import Optional

from pydantic import BaseModel

from asyncio import current_task
from sqlalchemy import text, create_engine
from sqlalchemy.orm import sessionmaker, declared_attr
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_scoped_session,
    AsyncSession,
    async_sessionmaker,
)
from sqlalchemy.exc import ProgrammingError, OperationalError

from config import settings
from app.utils.log import log


class CommonBase:
    """
    https://docs.sqlalchemy.org/en/13/orm/extensions/declarative/mixins.html
    """

    @classmethod
    @declared_attr
    def __tablename__(cls):
        """
        使用 @declared_attr 装饰器修饰 __tablename__ 类方法
        使得在每个继承 CustomBase 的子类中都会自动设置表名为该子类的类名（小写形式）
        """
        return cls.__name__.lower()


class Base(DeclarativeBase, CommonBase):
    """数据模型 基类"""

    pass


class DBEngine(Enum):
    MYSQL = "mysql"
    MYSQL_ASYNC = "aiomysql"
    POSTGRESQL = "postgresql"
    SQLITE = "sqlite"


class DBConfig(BaseModel):
    ENGINE: DBEngine
    HOST: str
    PORT: int = 3306
    USERNAME: str
    PASSWORD: str
    DATABASE: str


"""初始化 数据库配置"""
init_db_config = DBConfig(
    ENGINE=DBEngine.MYSQL,
    HOST=settings.MYSQL.HOST,
    PORT=settings.MYSQL.PORT,
    USERNAME=settings.MYSQL.USERNAME,
    PASSWORD=settings.MYSQL.PASSWORD,
    DATABASE=settings.MYSQL.DATABASE,
)


class DatabaseHelper:
    def __init__(self, config: DBConfig):
        self.config = config
        self.db_url = self.get_db_url(self.config)

        self.engine = None
        self.session = None
        self.async_engine = None
        self.async_session = None

    @classmethod
    def create(cls, config: DBConfig):
        instance = cls(config)
        instance.engine = create_engine(instance.db_url)
        instance.session = sessionmaker(instance.engine)
        instance.init_database()
        return instance

    @classmethod
    def create_async(cls, config: DBConfig) -> Optional["DatabaseHelper"]:
        if config.ENGINE != DBEngine.MYSQL_ASYNC:
            msg = "创建异步连接，检查数据库 engine 配置！"
            log.error(msg)
            raise NotImplementedError(msg)

        instance = cls(config)
        instance.async_engine = create_async_engine(
            instance.db_url,
            max_overflow=0,  # 连接池中允许溢出连接的最大数量，0 为不允许
            pool_size=50,  # 同时保持的最大连接数
            pool_recycle=1500,  # 连接的回收时间
            echo=True,
        )
        instance.async_session = async_scoped_session(
            async_sessionmaker(
                instance.async_engine, class_=AsyncSession, expire_on_commit=False
            ),
            scopefunc=current_task,
        )
        # await instance.init_database_async()
        return instance

    async def create_async_session(self) -> AsyncSession:
        async with self.async_session as session:
            return session

    def init_database(self):
        try:
            engine = create_engine(self.db_url)
            conn = engine.connect()
        except ProgrammingError:
            # 不存在则创建
            log.debug("初始化数据库: 🌐新建数据库中...")
            engine = create_engine(
                self.db_url.replace(self.config.DATABASE, ""),
                echo=False,  # 打印 sql 语句
            )

            sql = text(
                f"CREATE DATABASE IF NOT EXISTS {self.config.DATABASE} "
                f"default character set utf8mb4 collate utf8mb4_unicode_ci"
            )
            conn = engine.connect()
            conn.execute(sql)
        else:
            engine.dispose()
            log.debug(
                f"初始化数据库: ✅初始化完成「{self.config.DATABASE}」, 关闭连接。"
            )

    async def init_database_async(self):
        try:
            with self.async_session() as session:
                # 通过执行一个简单的 SQL 查询来检查数据库是否存在
                await session.execute("SELECT 1")
        except (OperationalError, ProgrammingError):
            log.debug("初始化数据库: 🌐新建数据库中...")
            async with self.async_session() as session:
                await session.execute(
                    text(
                        f"CREATE DATABASE IF NOT EXISTS {self.config.DATABASE} "
                        f"default character set utf8mb4 collate utf8mb4_unicode_ci"
                    )
                )
                await session.commit()
        else:
            # await self.dispose()
            log.debug(f"初始化数据库: ✅数据库初始化完成「{self.config.DATABASE}」")

    async def init_tables(self):
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            log.debug("初始化数据库: ✅所有表初始化完成 ~")

    @staticmethod
    async def connection_test(session: sessionmaker):
        if session is None:
            raise Exception("session 为空，数据库连接失败！")
        async with session() as s:
            await s.execute("SELECT 1")
            log.info("数据库连接测试通过！")

    @staticmethod
    def get_db_url(config: DBConfig) -> str:
        engine_enum = DBEngine(config.ENGINE)

        suffix = (
            f"{config.USERNAME}:"
            f"{config.PASSWORD}@{config.HOST}:"
            f"{config.PORT}/{config.DATABASE}"
        )

        if engine_enum == DBEngine.MYSQL:
            return f"mysql+mysqlconnector://{suffix}"
        elif engine_enum == DBEngine.MYSQL_ASYNC:
            return f"mysql+aiomysql://{suffix}"
        elif engine_enum == DBEngine.POSTGRESQL:
            return f"postgresql+asyncpg://{suffix}"
        elif engine_enum == DBEngine.SQLITE:
            return f"sqlite:///{config.DATABASE}"
        else:
            raise ValueError("Invalid DBConfig ENGINE value!")


DatabaseHelper.create(init_db_config)
async_config = deepcopy(init_db_config)
async_config.ENGINE = DBEngine.MYSQL_ASYNC
db_helper = DatabaseHelper.create_async(async_config)
async_engine = db_helper.async_engine
async_session = db_helper.async_session
