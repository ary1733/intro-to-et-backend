from src import db

class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(255), unique=True, nullable=False)
    isTrained = db.Column(db.Boolean, nullable=False)
    # One to many relationship, one Category will have multiple posts
    posts = db.relationship('Post',backref='categories')
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}