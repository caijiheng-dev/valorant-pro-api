import datetime
import uuid

from fastapi import HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User, UserToken
from schemas.user import UserRequest, UserUpdateRequest, UserChangePasswordRequest
from utils import password_security
from utils.password_security import get_hash_pwd


#根据用户名查询数据库
async def get_user_by_username(db:AsyncSession,username: str):
    query = select(User).where(User.username == username)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db:AsyncSession,user_data:UserRequest):
    #先密码加密->add
    hash_pwd = password_security.get_hash_pwd(user_data.password)
    user = User(username=user_data.username, password=hash_pwd)
    db.add(user)
    await db.commit()
    await db.refresh(user)#从数据库读回最新的user对象
    return user

#生成token

async def create_token(db:AsyncSession,user_id: str):
    #生成token->设置过期时间->查询数据库当前用户是否有token->有：更新，没有：添加
    token = str(uuid.uuid4())
    expires_at = datetime.datetime.now() + datetime.timedelta(hours=24)
    query = select(UserToken).where(UserToken.user_id == user_id)
    result = await db.execute(query)
    user_token = result.scalar_one_or_none()

    if user_token:
        user_token.token = token
        user_token.expires_at = expires_at
    else:
        user_token = UserToken(user_id=user_id, token=token,expires_at=expires_at)
        db.add(user_token)
    await db.commit()
    return token

#验证用户和密码
async def authenticate_user(db:AsyncSession,username:str,password:str):
    user = await get_user_by_username(db,username)
    if not user:
        return None
    if not password_security.verify_password(password,user.password):
        return None
    return user

#验证token->检查用户
async def get_user_by_token(db:AsyncSession,token:str):
    query = select(UserToken).where(UserToken.token == token)
    result = await db.execute(query)
    db_token = result.scalar_one_or_none()

    if not db_token or db_token.expires_at < datetime.datetime.now():
        return None

    query = select(User).where(User.id == db_token.user_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()

#更新用户信息
async def update_user(db:AsyncSession,username:str,user_data:UserUpdateRequest):
    query = update(User).where(User.username == username).values(**user_data.dict(
        exclude_none=True,
        exclude_unset=True
    ))
    result = await db.execute(query)
    await db.commit()
    #检查更新
    if result.rowcount==0:
        raise HTTPException(status_code=404, detail="User not found")
    #若更新成功，返回更新后的用户信息
    updated_user = await get_user_by_username(db,username)
    return updated_user

#修改密码
async def update_password(db:AsyncSession,user:User,old_password:str,new_password:str):
    #先验证旧密码是否正确
    if not password_security.verify_password(old_password,user.password):
        return False
    #若旧密码正确，开始修改密码
    hashed_password = get_hash_pwd(new_password)
    user.password = hashed_password
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return True
