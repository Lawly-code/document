import time

import jwt
from config import settings


class JWTRepository:
    def __init__(self):
        self.secret_key = settings.jwt_settings.secret_key
        self.algorithm = settings.jwt_settings.algorithm
        self.access_token_expire_minutes = (
            settings.jwt_settings.access_token_expire_minutes
        )
        self.refresh_token_expire_minutes = (
            settings.jwt_settings.refresh_token_expire_minutes
        )

    def sign_jwt(self, user_id: int) -> str:
        payload = {
            "user_id": user_id,
            "expires": time.time() + self.access_token_expire_minutes * 60,
        }
        token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

        return token

    def decode_jwt(self, token: str):
        """
        :param token: jwt token
        :return:
        :rtype: None | dict
        """
        try:
            decoded_token = jwt.decode(
                token, self.secret_key, algorithms=[self.algorithm]
            )
        except Exception:
            return None
        return decoded_token if decoded_token["expires"] >= time.time() else None
