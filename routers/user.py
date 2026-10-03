from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from config.db_config import get_db
from models.user import User
from schemas.user import UserRequest, UserAuthResponse, UserInfoResponse, UserUpdateRequest, UserChangePasswordRequest
from crud import user
from utils.auth import get_current_user
from utils.response import success_response

router = APIRouter(prefix="/api/user", tags=["user"])

#用户注册
@router.post("/register")
async def register(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    #注册逻辑：验证用户是否存在->创建用户->生成token->响应结果
    existing_user = await user.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="用户已存在")
    now_user = await user.create_user(db,user_data)
    token = await user.create_token(db,now_user.id)
    # return {
    #     "code":200,
    #     "message":"注册成功",
    #     "data":{
    #         "token":token,
    #         "userInfo":{
    #             "id":now_user.id,
    #             "username":now_user.username,
    #             "bio":now_user.bio,
    #             "avatar":now_user.avatar
    #         }
    #     }
    # }
    response_data = UserAuthResponse(token=token,user_info=UserInfoResponse.from_orm(now_user))
    return success_response(message="注册成功",data=response_data)

#用户登录
@router.post("/login")
async def login(user_data:UserRequest,db:AsyncSession = Depends(get_db)):
    #用户是否存在->密码是否正确->生成token->返回结果
    now_user = await user.authenticate_user(db,user_data.username,user_data.password)
    if not now_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="用户名或密码错误")
    token = await user.create_token(db,now_user.id)
    response_data = UserAuthResponse(token=token,user_info=UserInfoResponse.from_orm(now_user))
    return success_response(message="成功登录",data=response_data)

#用户信息获取
@router.get("/info")
async def get_user_info(now_user:User = Depends(get_current_user)):
    return success_response(message="获取用户信息成功",data = UserInfoResponse.from_orm(now_user))

#修改用户信息
@router.put("/update")
async def update_user_info(user_data:UserUpdateRequest,now_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    the_user = await user.update_user(db,now_user.username,user_data)
    return success_response(message="用户信息更新成功",data=UserInfoResponse.from_orm(the_user))

@router.put("/password")
async def update_password(password_data:UserChangePasswordRequest,now_user:User = Depends(get_current_user),db:AsyncSession = Depends(get_db)):
    res_update_pwd = await user.update_password(db,now_user,password_data.old_password,password_data.new_password)
    if not res_update_pwd:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail = "旧密码输入错误")
    return success_response(message="修改密码成功")