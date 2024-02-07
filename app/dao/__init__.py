"""
数据访问层 主要完成 crud 工作
"""

from typing import List

from app.utils.log import log
from app.models import async_session, Base as TableModel


class BaseDao:
    session = async_session
    model = None  # 在子类中定义具体的模型类

    async def create(self, instance: TableModel = None, **kwargs):
        """向表格插入数据，支持直接传入 Base 或 dict"""
        async with self.session() as session:
            if instance is None:
                instance = self.model(**kwargs)
            session.add(instance)
            await session.commit()
            return instance

    async def read(self, sql) -> List:
        async with self.session() as session:
            result = await session.execute(sql)
            return result.scalars().all()

    async def update(self, sql):
        async with self.session() as session:
            await session.execute(sql)
            await session.commit()

    async def delete(self, sql):
        async with self.session() as session:
            await session.execute(sql)
            await session.commit()

    async def execute_begin(self, sql, error_msg: str = None):
        try:
            async with self.session() as session:
                async with session.begin():  # begin 事务
                    await session.execute(sql)
        except Exception as e:
            if error_msg is None:
                error_msg = f"执行 SQL 事务异常: {str(e)}"
            log.error(error_msg)
            raise Exception(error_msg)
