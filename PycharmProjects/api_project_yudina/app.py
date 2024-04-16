from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.orm import Session


from database import *
from table_feed import Feed
from table_post import Post
from table_user import User

from sqlalchemy import *

from schema import *

app = FastAPI()

def get_db():
    with SessionLocal() as db:
        return db

@app.get("/user/{id}", response_model=UserGet)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    id_query = db.query(User).filter(User.id == id).first()
    if not id_query:
        raise HTTPException(status_code=404)
    return id_query

@app.get("/post/{id}", response_model=PostGet)
def get_post_by_id(id: int, db: Session = Depends(get_db)):
    id_query = db.query(Post).filter(Post.id == id).first()
    if not id_query:
        raise HTTPException(status_code=404)
    return id_query

@app.get("/user/{id}/feed", response_model=List[FeedGet])
def get_user_id_feed(id: int, db: Session = Depends(get_db), limit: int = 10):
    feed_user_query = db.query(Feed).filter(Feed.user_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_user_query:
        return Response(content=[], status_code=200)
    return feed_user_query

@app.get("/post/{id}/feed", response_model=List[FeedGet])
def get_post_id_feed(id: int, db: Session = Depends(get_db), limit: int = 10):
    feed_post_query = db.query(Feed).filter(Feed.post_id == id).order_by(Feed.time.desc()).limit(limit).all()
    if not feed_post_query:
        return Response(content=[], status_code=200)
    return feed_post_query


@app.get("/post/recommendations/", response_model=List[PostGet])
def get_post_recommendation(id: int, db: Session = Depends(get_db), limit: int = 10):
    get_post_recommendation_query = db.query(Feed.post_id, func.count(Feed.post_id)).filter(
        Feed.action == 'like').group_by(Feed.post_id).order_by(func.count(Feed.post_id).desc()).limit(limit).all()

    recommendations = []
    for post_id, count in get_post_recommendation_query:
        post = db.query(Post).filter(Post.id == post_id).first()
        if post:
            recommendations.append(PostGet(id=post.id, text=post.text, topic=post.topic))

    return recommendations







