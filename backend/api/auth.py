from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional, Any
import time
import base64
import json

from backend.db.users import MOCK_USERS

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class ResetPasswordRequest(BaseModel):
    username: str
    new_password: str

class LoginResponse(BaseModel):
    token: str
    username: str
    role: str
    customers: List[Any]
    name: str
    live_sync: bool = False

class UserProfile(BaseModel):
    username: str
    role: str
    customers: List[Any]
    name: str
    live_sync: bool = False

# In a real application, use OAuth2PasswordBearer and JWT tokens (e.g. pyjwt)
def create_mock_token(username: str) -> str:
    # A simple base64 encoded JSON string for demo purposes
    payload = {
        "sub": username,
        "exp": int(time.time()) + 3600 * 24 # 24 hours
    }
    payload_str = json.dumps(payload)
    return base64.b64encode(payload_str.encode()).decode()

def decode_mock_token(token: str) -> Optional[str]:
    try:
        payload_str = base64.b64decode(token).decode()
        payload = json.loads(payload_str)
        if payload["exp"] < int(time.time()):
            return None # Expired
        return payload["sub"]
    except Exception:
        return None

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest):
    user = MOCK_USERS.get(request.username)
    if not user or user["password"] != request.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_mock_token(request.username)
    
    customers_list = user["customers"]
    if user.get("live_sync", False) or request.username == "Shah.Manank":
        try:
            from backend.api_client.crm_rest_client import CRMRestClient
            from pathlib import Path
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                client = CRMRestClient(api_url="mock", api_token="mock", downloads_dir=Path(tmpdir), logged_in_user=request.username)
                live_customers = client.get_customers()
                if live_customers:
                    customers_list = live_customers
        except Exception as e:
            import traceback
            print(f"Exception during live sync in login: {e}")
            traceback.print_exc()
            pass
            
    return LoginResponse(
        token=token,
        username=request.username,
        role=user["role"],
        customers=customers_list,
        name=user["name"],
        live_sync=user.get("live_sync", False)
    )

@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    if request.username not in MOCK_USERS:
        raise HTTPException(status_code=404, detail="Username not found")
        
    current_user = MOCK_USERS[request.username]
    if current_user["password"] == request.new_password:
        raise HTTPException(status_code=400, detail="New password cannot be the same as the old password")
        
    # Update in memory
    current_user["password"] = request.new_password
    
    # Persist to users.py file for perfectly working demo across server restarts
    try:
        import os
        from pathlib import Path
        db_path = Path(__file__).parent.parent / "db" / "users.py"
        
        with open(db_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        # We'll use a simple regex to replace the specific user's password string
        import re
        # This is a bit fragile but works for our specific mock db structure
        pattern = f'"{request.username}":\s*{{\s*"password":\s*"[^"]*"'
        replacement = f'"{request.username}": {{\n        "password": "{request.new_password}"'
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(db_path, "w", encoding="utf-8") as f:
            f.write(new_content)
            
        return {"status": "success", "message": "Password reset successfully"}
    except Exception as e:
        print(f"Failed to persist password to disk: {e}")
        # Still return success since in-memory is updated
        return {"status": "success", "message": "Password reset temporarily for this session"}

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> UserProfile:
    username = decode_mock_token(token)
    if not username or username not in MOCK_USERS:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = MOCK_USERS[username]
    customers_list = user["customers"]
    if user.get("live_sync", False) or username == "Shah.Manank":
        try:
            from backend.api_client.crm_rest_client import CRMRestClient
            from pathlib import Path
            import tempfile
            with tempfile.TemporaryDirectory() as tmpdir:
                client = CRMRestClient(api_url="mock", api_token="mock", downloads_dir=Path(tmpdir), logged_in_user=username)
                live_customers = client.get_customers()
                if live_customers:
                    customers_list = live_customers
        except Exception as e:
            pass
            
    return UserProfile(
        username=username,
        role=user["role"],
        customers=customers_list,
        name=user["name"],
        live_sync=user.get("live_sync", False)
    )

@router.get("/me", response_model=UserProfile)
def read_users_me(current_user: UserProfile = Depends(get_current_user)):
    return current_user

def require_admin(current_user: UserProfile = Depends(get_current_user)) -> UserProfile:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin privileges required."
        )
    return current_user
