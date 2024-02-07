"""
对象模型定义
"""
from typing import Optional, TypeVar

from app.models import BaseModel

# TypeVar 可以用来定义一个抽象的类型参数，它表示一组类型之一，用于创建类型变量
# DBModel 用于限定继承于 Model 的模型类
DBModel = TypeVar("DBModel", bound=BaseModel)

