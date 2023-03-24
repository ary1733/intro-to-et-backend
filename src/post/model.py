from src import db

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    imgLink = db.Column(db.String(255), nullable=False)
    unixTime = db.Column(db.Integer, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    userId = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    categoryId = db.Column(db.Integer,db.ForeignKey("categories.id"), nullable=False)
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}