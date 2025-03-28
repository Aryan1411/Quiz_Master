from flask import current_app as app
from .database import db

#Creating the database model
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    username=db.Column(db.String(120), unique=True, nullable=False)
    password=db.Column(db.String(80), nullable=False)
    qualification=db.Column(db.String(80), nullable=False)
    dob=db.Column(db.String(80), nullable=False)
    type=db.Column(db.String(80), nullable=False)
    scores=db.relationship('Scores', backref='user', lazy=True)
    def __init__(self, name, username, password, qualification, dob, type):
        self.name=name
        self.username=username
        self.password=password
        self.qualification=qualification
        self.dob=dob
        self.type=type
class Subject(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    sdesc=db.Column(db.String(120), nullable=True)
    chapters=db.relationship('Chapter', backref='subject', lazy=True)
    def __init__(self, name,sdesc):
        self.name=name
        self.sdesc=sdesc
class Chapter(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(80), unique=True, nullable=False)
    cdesc=db.Column(db.String(120), nullable=True)
    sub_id=db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    quiz=db.relationship('Quiz', backref='chapter', lazy=True)
    def __init__(self, name,cdesc,sub_id):
        self.name=name
        self.cdesc=cdesc
        self.sub_id=sub_id
class Quiz(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    chapter_id=db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    date_of_quiz=db.Column(db.Date, nullable=False)
    time_duration=db.Column(db.Time, nullable=False)
    remarks=db.Column(db.String(120), nullable=True)
    questions=db.relationship('Question', backref='quiz', lazy=True)
    scores=db.relationship('Scores', backref='quiz', lazy=True)
    def __init__(self, chapter_id,date_of_quiz,time_duration,remarks):
        self.chapter_id=chapter_id
        self.date_of_quiz=date_of_quiz
        self.time_duration=time_duration
        self.remarks=remarks

class Question(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    quiz_id=db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    que_statement=db.Column(db.String(120), nullable=False)
    option_1=db.Column(db.String(80), nullable=False)
    option_2=db.Column(db.String(80), nullable=False)
    option_3=db.Column(db.String(80), nullable=False)
    option_4=db.Column(db.String(80), nullable=False)
    ans=db.Column(db.String(80), nullable=False)
    def __init__(self, quiz_id,que_statement,option_1,option_2,option_3,option_4,ans):
        self.quiz_id=quiz_id
        self.que_statement=que_statement
        self.option_1=option_1
        self.option_2=option_2
        self.option_3=option_3
        self.option_4=option_4
        self.ans=ans
class Scores(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id=db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    time_stamp=db.Column(db.DateTime, nullable=False)
    total_scored=db.Column(db.Integer, nullable=False)
    def __init__(self, user_id,quiz_id,time_stamp,total_scored):
        self.user_id=user_id
        self.quiz_id=quiz_id
        self.time_stamp=time_stamp
        self.total_scored=total_scored

