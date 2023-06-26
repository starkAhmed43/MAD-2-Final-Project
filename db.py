from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin,RoleMixin
from dataclasses import dataclass
from datetime import datetime

db=SQLAlchemy()

roles_users = db.Table("roles_users",db.Column("user_id",db.Integer(),db.ForeignKey("user.id")),
										db.Column("role_id",db.Integer(),db.ForeignKey("role.id")))

@dataclass
class User(db.Model,UserMixin):
	id : int
	email : str
	password : str

	__tablename__="user"
	id=db.Column(db.Integer(),primary_key=True)
	email = db.Column(db.String(),unique=True,nullable=False)
	password = db.Column(db.String(),nullable=False)
	active = db.Column(db.Boolean())
	fs_uniquifier = db.Column(db.String(255), unique=True, nullable=False)
	roles = db.relationship("Role",secondary=roles_users,backref=db.backref("users",lazy="dynamic"))

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)

	def __repr__(self):
		return f'User:: id:{self.id}, email:{self.email}'

class Role(db.Model,RoleMixin):
	id=db.Column(db.Integer(),primary_key=True)
	name=db.Column(db.String())
	description=db.Column(db.String())


@dataclass
class Deck(db.Model):
	id : int
	name : str
	user_id : int
	last_reviewed : datetime
	total_score : int

	__tablename__="deck"
	id=db.Column(db.Integer(),primary_key=True)
	name=db.Column(db.String(),nullable=False)
	user_id=db.Column(db.Integer(),db.ForeignKey("user.id"))
	last_reviewed=db.Column(db.DateTime(),default=datetime.now())
	total_score=db.Column(db.Integer(),default=0)

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)

	def __repr__(self):
		return f'Deck:: id:{self.id}, name:{self.name}, user_id:{self.user_id}, last_reviewed:{self.last_reviewed}, total_score:{self.total_score}'	

@dataclass
class Card(db.Model):
	id : int
	deck_id : int
	question : str
	answer : str
	difficulty : str
	last_reviewed : datetime
	last_score : int

	__tablename__="card"
	id=db.Column(db.Integer(),primary_key=True)
	deck_id=db.Column(db.Integer,db.ForeignKey("deck.id"))
	question=db.Column(db.String(),nullable=False)
	answer=db.Column(db.String(),nullable=False)
	difficulty=db.Column(db.String(),default="None")
	last_reviewed=db.Column(db.DateTime(),default=datetime.now())
	last_score=db.Column(db.Integer(),default=0)

	def __init__(self, *args, **kwargs):
		super().__init__(*args,**kwargs)

	def __repr__(self):
		return f'Card:: id:{self.id}, deck_id:{self.deck_id}, question:{self.question}, answer:{self.answer}, difficulty:{self.difficulty}, last_reviewed:{self.last_reviewed}, last_score:{self.last_score}'


