from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import jwt, time

from keys import KeyManagement

# initialize FastAPI app
app = FastAPI()  

# instance of KeyManagement
manager = KeyManagement()  

# generate one active and one expired key
active_key = manager.create_new_key()
expired_key = manager.create_new_key(expired=True)

# Root Endpoint
@app.get("/")
def root():
    return {
        "message": "JWKS Server is running",
        "endpoints": {
            "JWKS": "/.well-known/jwks.json",
            "Auth": "/auth"
        }
    }

# JWKS Endpoint
@app.get("/.well-known/jwks.json")
# return JWKS (set of public keys) in JSON format 
def get_active_keys():
    # only return active keys (exclude expired ones)
    active = manager.get_active_keys()
    jwks = {"keys": [manager.convert_to_jwk(k) for k in active]}
    return JSONResponse(content=jwks)

# Auth Endpoint
@app.post("/auth")
async def auth(request: Request):
    """
    Return a JWT signed with either active or expired key.
    Use ?expired=true to request expired JWT.
    """
    use_expired = request.query_params.get("expired") == "true"  

    current_time = int(time.time())
    if use_expired:
        # use the expired key
        key = expired_key
        exp_time = key["exp"]  # already expired
    else:
        # use the active key
        key = active_key
        exp_time = key["exp"]

    payload = {
        "sub": "fakeuser",   # subject
        "iat": current_time, # issue at
        "exp": exp_time      # expiry time
    }

    # sign the JWT with the chosen private key, include kid in header
    token = jwt.encode(
        payload,
        key["private"],       # use correct private key
        algorithm="RS256",
        headers={"kid": key["kid"]}
    )

    return {"token": token}
