from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import User, Auth
from app.schemas.auth_schemas import (
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
)
from app.services.password import hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=RegisterResponse)
def register_user(payload: RegisterRequest, db: Session = Depends(get_db)):
    # 1. Check if user already exists
    existing_user = db.query(User).filter(User.email == payload.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists."
        )

    # 2. Create a new user in 'users' table
    new_user = User(
        name=payload.name,
        contact=payload.contact,
        email=payload.email,
        company=payload.company
    )
    db.add(new_user)
    db.flush()  # flush to get new_user.user_id from DB

    # 3. Hash the password & create 'auth' record
    hashed_pw = hash_password(payload.password)
    auth_record = Auth(
        user_id=new_user.user_id,
        encrypted_password=hashed_pw,
        role=payload.role
    )
    db.add(auth_record)
    db.commit()

    return RegisterResponse(
        user_id=str(new_user.user_id),
        message="User registered successfully"
    )

@router.post("/login", response_model=LoginResponse)
def login_user(payload: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    auth_record = db.query(Auth).filter(Auth.user_id == user.user_id).first()
    if not auth_record or not verify_password(payload.password, auth_record.encrypted_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password."
        )

    return LoginResponse(
        user_id=str(user.user_id),
        role=auth_record.role,
        message="Login successful"
    )
