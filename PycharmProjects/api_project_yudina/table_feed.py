from sqlalchemy.orm import relationship

from database import *
from table_post import Post
from table_user import User

from sqlalchemy import *

class Feed(Base):
    __tablename__ = 'feed_action'
    action = Column(String)
    post_id = Column(Integer, ForeignKey(Post.id), primary_key=True)
    time = Column(TIMESTAMP(timezone=False))
    user_id = Column(Integer, ForeignKey(User.id), primary_key=True)
    user = relationship(User)
    post = relationship(Post)
