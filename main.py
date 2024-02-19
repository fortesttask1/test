from fastapi import FastAPI
from sqlalchemy.orm import Session

from crud import crud
from db.database import Base, engine, SessionLocal
from routers import item_routes, user_routes, login, category_routes
from schemas.user import SuperUserCreate

app = FastAPI()

app.include_router(login.router, tags=['login'])
app.include_router(item_routes.router, tags=['item'])
app.include_router(user_routes.router, tags=['user'])
app.include_router(category_routes.router, tags=['category'])

Base.metadata.create_all(bind=engine)

#
# def create_superuser(email: str, username: str, password: str):
#     db: Session = SessionLocal()
#     user_in = SuperUserCreate(
#         email=email,
#         username=username,
#         password=password,
#         is_superuser=True,
#     )
#     user = crud.user.get_by_email(db, email=email)
#     if user:
#         print(f"User with email {email} already exists. Cannot create superuser.")
#         return
#     user = crud.user.create_super_user(db, obj_in=user_in)
#     db.commit()
#     db.refresh(user)
#     print(f"Superuser with email {email} created.")
#     db.close()
#
#
# create_superuser(email="user12@example.com", username="admin12", password="password")
