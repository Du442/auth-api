from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from db import get_db
from models import User
from schemas import UserLoginSchema
import jwt, os


load_dotenv()

secret_key = os.getenv("SECRET_KEY")

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        decodex = jwt.decode(token, secret_key, algorithms=['HS256'])

        user = db.query(User).filter(User.mail == decodex['sub']).first()

        if not user:
            raise HTTPException(status_code=401, detail='Token inválido')

        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(401, detail="Token Inválido")
    
@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/users/")
async def read_users(usuario_atual: User = Depends(get_current_user)):
    return {"email_logado": usuario_atual.mail, "role": usuario_atual.role}

@app.post("/auth/login")
def login(dados_login: UserLoginSchema, db: Session = Depends(get_db)):

    # busca o usuário no banco pelo e-mail
    user = db.query(User).filter(User.mail == dados_login.email).first()

    # se o usuário existir, usa o metodo da classe para verificar a senha
    if not user or not user.verify_password(dados_login.password):
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    # se a senha estiver correta, gera o token
    dados_do_payload = {
        "sub":user.mail,
        "role":user.role,
        "exp":datetime.now(timezone.utc) + timedelta(minutes=30)
    }

    token_gerado = jwt.encode(dados_do_payload, secret_key, algorithm="HS256")

    return {"access_token": token_gerado, "token_type": "bearer"}