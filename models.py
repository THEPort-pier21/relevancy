from app import db

class Data(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  url = db.Column(db.String)
  text = db.Column(db.String)
  relevancy = db.Column(db.String)
  cluster = db.Column(db.String)
  feedback_relevancy = db.Column(db.String)
  feedback_cluster = db.Column(db.String)
