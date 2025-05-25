from fastapi import APIRouter, HTTPException, status
from api.v1.models.auth import Token, UserLogin
from core.security import create_access_token
from core.config import settings

router = APIRouter()

@router.post("/login", response_model=Token, summary="Realiza login e retorna um token JWT")
async def login_for_access_token(user: UserLogin):
    if user.username == settings.TEST_USERNAME and user.password == settings.TEST_PASSWORD:
        access_token = create_access_token(user.username)
        return {"access_token": access_token, "token_type": "bearer"}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )