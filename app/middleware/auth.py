"""
JWT TOKEN 生成与解析
"""
import jwt
import hashlib
from datetime import timedelta, datetime

from config import settings


class JWTAuth:
    def __init__(self):
        self.salt = settings.AUTH.SALT
        self.secret_key = settings.AUTH.KEY
        self.algorithm = "HS256"
        self.expires_hour = settings.AUTH.EXPIRED_HOUR

    def generate_token(self, payload: dict) -> str:
        expiration_time = datetime.utcnow() + timedelta(hours=self.expires_hour)
        payload["exp"] = expiration_time
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            # Token 过期
            return {"error": "登录状态已过期, 请重新登录"}
        except jwt.InvalidTokenError:
            # Token 无效
            return {"error": "登录状态校验失败, 请重新登录"}

    @staticmethod
    def add_salt(password):
        m = hashlib.md5()
        bt = f"{password}{settings.AUTH.SALT}".encode("utf-8")
        m.update(bt)
        return m.hexdigest()


if __name__ == "__main__":
    jwt_auth = JWTAuth()

    # 生成令牌
    token_payload = {"user_id": 123, "username": "example"}
    token = jwt_auth.generate_token(token_payload)
    print("Generated token:", token)

    # 解码令牌
    decoded_payload = jwt_auth.decode_token(token)
    print("Decoded payload:", decoded_payload)

    print(jwt_auth.add_salt("test"))
