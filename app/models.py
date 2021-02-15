from app import db
from sqlalchemy import func

class Submissions(db.Model):
  idstr = db.Column(db.Text, primary_key=True, index=True, unique=True)
  created = db.Column(db.Integer)
  isself = db.Column('self', db.Boolean)
  nsfw = db.Column(db.Boolean)
  author = db.Column(db.Text)
  title = db.Column(db.Text)
  url = db.Column(db.Text)
  selftext = db.Column(db.Text)
  score = db.Column(db.Integer)
  subreddit = db.Column(db.Text, index=True)
  num_comments = db.Column(db.Integer)
  comments = db.relationship('Comments', lazy='dynamic')

  def __repr__(self):
    return '<Submission {}>'.format(self.idstr)


class Comments(db.Model):
  idstr = db.Column(db.Text, primary_key=True, index=True, unique=True)
  created = db.Column(db.Integer)
  author = db.Column(db.Text)
  body = db.Column(db.Text)
  score = db.Column(db.Integer)
  subreddit = db.Column(db.Text, index=True)
  parent = db.Column(db.Text)
  submission = db.Column(db.Text, db.ForeignKey('submissions.idstr'), nullable=False)

  @property
  def serialize(self):
    return {
      'idstr': self.idstr,
      'created': self.created,
      'author': self.author,
      'body': self.body,
      'score': self.score,
      'parent': self.parent,
    }

  def __repr__(self):
    return '<Comment {}>'.format(self.idstr)


# https://gist.github.com/hest/8798884
def get_count(q):
  count_q = q.statement.with_only_columns([func.count()]).order_by(None)
  count = q.session.execute(count_q).scalar()
  return count
