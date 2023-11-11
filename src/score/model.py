from src import db

class Score(db.Model):
    __tablename__ = "scores"
    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.Integer, nullable=False)
    #  float time taken
    timetaken = db.Column(db.Float, nullable=False)
    # unixTime = db.Column(db.Integer, nullable=False)
   
    userId = db.Column(db.Integer,db.ForeignKey("users.id"), nullable=False)
    # __table_args__ = (
    #     db.Index('scores_unixTime_idx', unixTime.desc()),
    # )
    def as_dict(self):
        dict = {}
        for c in self.__table__.columns:
                dict[c.name] = getattr(self, c.name)
        return dict