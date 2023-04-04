from src import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role= db.Column(db.String(255), nullable=False, default='USER')

    # One to many relationship, one user will have multiple posts
    posts = db.relationship('Post',backref='users')
    
    def as_dict(self):
       return {c.name: getattr(self, c.name) for c in self.__table__.columns}