import jwt
from datetime import datetime, timedelta

SECRET_KEY = "secret_key_for_jwt"

def generate_token(user_id):
    expiration = datetime.utcnow() + timedelta(hours=1)
    token = jwt.encode(
        {"user_id": user_id, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256"
    )
    return token

def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["user_id"]
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
