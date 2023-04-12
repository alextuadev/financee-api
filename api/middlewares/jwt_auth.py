from fastapi.security import HTTPBearer
from fastapi import Request, HTTPException
from utils.jwt_manager import verify_access_token

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        auth = await super().__call__(request)
        return verify_access_token(auth.credentials, request)