from passlib.context import CryptContext

#创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#密码加密
def get_hash_pwd(pw:str):
    return pwd_context.hash(pw)

#验证密码
def verify_password(plain_password, hashed_password):
    # 布尔值
    return pwd_context.verify(plain_password, hashed_password)
