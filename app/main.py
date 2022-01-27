from typing import Optional, List

from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

from sqlalchemy.orm import Session
from . import models
from . import schemas
from . import utils 
from .database import engine, get_db
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', 
        password='*****', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfull")
        break
    except Exception as error:
        print("Connecting to Database")
        print("Error: ", error)
        time.sleep(2)

my_posts = [{"title": "title of post 1", "content": "content of post 1", "id": 1}, {
    "title": "favourite foods", "content": "I like fufu", "id": 2}]

def find_post(id):
    for post in my_posts:
        if post["id"] == id:
            return post

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Hi, Welcome to my API"}

