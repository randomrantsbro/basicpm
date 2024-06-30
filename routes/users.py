from fastapi import APIRouter, HTTPException
from ..models import User, UserResponse
from ..database import db
from app.gemini_client import GeminiClient
import random

router = APIRouter()
gemini_client = GeminiClient()


@router.post("/users", response_model=User)
def create_user(user: User):
    users = db.table('users').all()

    if any(u['id'] == user.id for u in users):
        raise HTTPException(status_code=400, detail="User ID already exists")

    if any(u['email'] == user.email for u in users):
        raise HTTPException(status_code=400, detail="Email already exists")

    user_id = random.randint(1, 100000)
    user.id = user_id
    db.table('users').insert(user.dict())
    print(user)
    return user

@router.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    users = db.table('users').all()
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(user)
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
def update_user(user_id: int, user: User):
    users = db.table('users').all()
    existing_user = next((u for u in users if u['id'] == user_id), None)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if existing_user['name'] == user.name and existing_user['email'] == user.email:
        return {"message": "Details are already up-to-date"}

    db.table('users').update(user.dict(), doc_ids=[existing_user.doc_id])
    return {"message": f"Details Updated Successfully for {user.name}"}

@router.delete("/users/{user_id}")
def delete_user(user_id: int):
    users = db.table('users').all()
    existing_user = next((u for u in users if u['id'] == user_id), None)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.table('users').remove(doc_ids=[existing_user.doc_id])
    return {"message": "User deleted"}

@router.get("/users/{user_id}/generate_prompted_content")
async def generate_prompted_content(user_id: int, prompt: str):
    # Fetch user details from database
    user = db.table('users').get(doc_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    content = gemini_client.generate_content(prompt)
    user['generated_content'] = content
    db.table('users').update(user, doc_ids=[user_id])

    return {"user_id": user_id, "generated_content": content}
