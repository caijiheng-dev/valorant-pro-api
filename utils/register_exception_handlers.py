from fastapi import FastAPI, HTTPException
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from utils.exception_handlers import (
    http_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
    general_exception_handler
)


def register_exception_handlers(app: FastAPI):
    """
    注册全局异常处理
    """
    # 业务异常（HTTPException）
    app.add_exception_handler(HTTPException, http_exception_handler)
    # 数据完整性约束异常（IntegrityError）
    app.add_exception_handler(IntegrityError, integrity_error_handler)
    # SQLAlchemy 数据库通用异常（SQLAlchemyError）
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
    # 兜底：所有未捕获的异常（Exception）
    app.add_exception_handler(Exception, general_exception_handler)
