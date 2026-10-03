#根据token查询用户。然后返回
from fastapi import Header, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from crud import user


async def get_current_user(authorization:str = Header(...),db:AsyncSession = Depends(get_db)):
    token = authorization.split(" ")[1]
    now_user = await user.get_user_by_token(db,token)
    if not now_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效令牌或令牌过期")

    return now_user