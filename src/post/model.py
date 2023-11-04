from src import db
from geoalchemy2 import Geometry

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    imgID = db.Column(db.String(255), nullable=False)
    unixTime = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    geometry = db.Column(Geometry(geometry_type='POINT'), nullable=False)
    userId = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    categoryId = db.Column(db.Integer,db.ForeignKey("categories.id"), nullable=False)
    __table_args__ = (
        db.Index('posts_unixTime_idx', unixTime.desc()),
    )
    
    def as_dict(self):
        dict = {}
        for c in self.__table__.columns:
            if(c.name!='geometry'):
                dict[c.name] = getattr(self, c.name)
        return dict