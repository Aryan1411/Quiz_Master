# Importing the required libraries
from flask import Flask, request, jsonify, render_template, redirect, url_for
from jinja2 import Template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date,time

#Initialising the flask app
app=Flask(__name__)

#Configuring the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

#Initialising the database
db=SQLAlchemy(app)




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

app.app_context().push()

#db.create_all() 







#Creating routes for the web app
@app.route('/')
def home():
    return render_template('home.html')

#Login Part

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user and user.type=='user':
            if user.password==password:
                return redirect("/user_dash/"+str(user.id))
            else:
                return "Invalid Password"
        else:
            return "Invalid Username"
    return render_template('login.html')

@app.route('/register',methods=['POST','GET'])
def register():
    if request.method=='POST':
        name=request.form['name']
        username=request.form['username']
        password=request.form['password']
        qualification=request.form['qual']
        dob=request.form['dob']
        user=User(name=name, username=username, password=password, qualification=qualification, dob=dob,type='user')
        db.session.add(user)
        db.session.commit()
        return render_template('login.html')
    return render_template('register.html')

@app.route('/admin',methods=['POST','GET'])
def admin():
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']
        user=User.query.filter_by(username=username).first()
        if user and user.type=='admin':
            if user.password==password:
                return redirect('/admin_dash')
            else:
                return "Invalid Password"
        else:
            return "Invalid Username"
    return render_template('admin_login.html')

#Admin Part

@app.route('/admin_dash',methods=['POST','GET'])
def admin_dash():
    users=User.query.filter_by(type='user').all()
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    quizzes=Quiz.query.all()
    questions=Question.query.all()
    return render_template('admin_dash.html',users=users,subjects=subjects,chapters=chapters,quizzes=quizzes,
                questions=questions)


@app.route('/admin/add_subject',methods=['POST','GET'])
def add_subject():
    if request.method=='POST':
        sname=request.form['sname']
        sdesc=request.form['sdesc']
        subjects=Subject.query.get(sname)
        if subjects:
            return "Subject already exists"
        subject=Subject(name=sname,sdesc=sdesc)
        db.session.add(subject)
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('add_subject.html')

@app.route('/admin/edit_subject/<int:id>',methods=['POST','GET'])
def edit_subject(id):
    subject=Subject.query.filter_by(id=id).first()
    if request.method=='POST':
        sname=request.form['sname']
        sdesc=request.form['sdesc']
        subject.name=sname
        subject.sdesc=sdesc
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('edit_subject.html',subject=subject)

@app.route('/admin/delete_subject/<int:id>',methods=['POST','GET'])
def delete_subject(id):
    subject=Subject.query.filter_by(id=id).first()
    if subject:
        chapters=Chapter.query.filter_by(sub_id=id).all()
        if chapters:
            for c in chapters:
                quiz=Quiz.query.filter_by(chapter_id=c.id).all()
                if quiz:
                    for q in quiz:
                        questions=Question.query.filter_by(quiz_id=q.id).all()
                        for que in questions:
                            db.session.delete(que)
                            db.session.commit()
                        db.session.delete(q)
                        db.session.commit()
                db.session.delete(c)
                db.session.commit()
        db.session.delete(subject)
        db.session.commit()
        return redirect('/admin_dash')
    else:
        return "Subject not found"
    
@app.route('/admin/add_chapter/<int:id>',methods=['POST','GET'])
def add_chapter(id):
    if request.method=='POST':
        cname=request.form['cname']
        cdesc=request.form['cdesc']
        chapters=Chapter.query.get(cname)
        if chapters:
            return "Chapter already exists"
        chapter=Chapter(name=cname,cdesc=cdesc,sub_id=id)
        db.session.add(chapter)
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('add_chapter.html')

@app.route('/admin/edit_chapter/<int:id>',methods=['POST','GET'])
def edit_chapter(id):
    chapter=Chapter.query.filter_by(id=id).first()
    if request.method=='POST':
        sname=request.form['cname']
        sdesc=request.form['cdesc']
        chapter.name=sname
        chapter.cdesc=sdesc
        db.session.commit()
        return redirect('/admin_dash')
    return render_template('edit_chapter.html',chapter=chapter)

@app.route('/admin/delete_chapter/<int:id>',methods=['POST','GET'])
def delete_chapter(id):
    chapter=Chapter.query.filter_by(id=id).first()
    if chapter:
        quiz=Quiz.query.filter_by(chapter_id=id).all()
        if quiz:
            for q in quiz:
                questions=Question.query.filter_by(quiz_id=q.id).all()
                for que in questions:
                    db.session.delete(que)
                    db.session.commit()
                db.session.delete(q)
                db.session.commit()
        db.session.delete(chapter)
        db.session.commit()
        return redirect('/admin_dash')
    else:
        return "Chapter not found"

@app.route('/admin_dash/quiz',methods=['POST','GET'])
def admin_quiz():
    quizes=Quiz.query.all()
    chapters=Chapter.query.all()
    return render_template('admin_dash_quiz.html',quizes=quizes,chapters=chapters,questions=Question.query.all())
@app.route('/admin_dash/add_quiz',methods=['POST','GET'])
def admin_add_quiz():
    if request.method=='POST':
        chapter_id=request.form['cname']
        date_of_quiz=datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        time_duration=datetime.strptime(request.form['time'], '%H:%M').time()
        remarks=request.form['remark']
        quiz=Quiz(chapter_id=chapter_id,date_of_quiz=date_of_quiz,time_duration=time_duration,remarks=remarks)
        db.session.add(quiz)
        db.session.commit()
        return redirect('/admin_dash/quiz')
    return render_template('add_quiz.html',chapters=Chapter.query.all())

@app.route("/admin_dash/quiz/delete/<int:id>")
def admin_delete_quiz(id):
    quiz=Quiz.query.filter_by(id=id).first()
    if quiz:
        score=Scores.query.filter_by(quiz_id=id).all()
        if score:
            for s in score:
                db.session.delete(s)
                db.session.commit()
        questions=Question.query.filter_by(quiz_id=id).all()
        if questions:
            for q in questions:
                db.session.delete(q)
                db.session.commit()
        db.session.delete(quiz)
        db.session.commit()
    return redirect('/admin_dash/quiz')

@app.route('/admin_dash/quiz/add_question/<int:id>',methods=['POST','GET'])
def add_question(id):
    if request.method=='POST':
        que=request.form['que']
        op1=request.form['op1']
        op2=request.form['op2']
        op3=request.form['op3']
        op4=request.form['op4']
        ans=request.form['ans']
        question=Question(quiz_id=id,que_statement=que,option_1=op1,option_2=op2,option_3=op3,option_4=op4,ans=ans)
        db.session.add(question)
        db.session.commit()
        return redirect('/admin_dash/quiz')
    return render_template('add_question.html')

@app.route('/admin_dash/quiz/edit_que/<int:id>',methods=['POST','GET'])
def edit_question(id):
    question=Question.query.filter_by(id=id).first()
    if request.method=='POST':
        que=request.form['que']
        op1=request.form['op1']
        op2=request.form['op2']
        op3=request.form['op3']
        op4=request.form['op4']
        ans=request.form['ans']
        question.que_statement=que
        question.option_1=op1
        question.option_2=op2
        question.option_3=op3
        question.option_4=op4
        question.ans=ans
        db.session.commit()
        return redirect('/admin_dash/quiz')
    return render_template('edit_que.html',question=question)

@app.route('/admin_dash/quiz/delete_que/<int:id>',methods=['POST','GET'])
def delete_question(id):
    question=Question.query.filter_by(id=id).first()
    if question:
        db.session.delete(question)
        db.session.commit()
    return redirect('/admin_dash/quiz')

@app.route('/admin_dash/summary',methods=['POST','GET'])
def admin_summary():
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    quizes=Quiz.query.all()
    questions=Question.query.all()
    scores=Scores.query.all()
    users=User.query.all()
    return render_template('admin_summary.html',scores=scores,users=users,chapters=chapters,quizes=quizes,questions=questions,subjects=subjects)
#Running the flask app
@app.route('/admin_dash/search',methods=['POST','GET'])
def admin_search():
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    quizes=Quiz.query.all()
    questions=Question.query.all()
    scores=Scores.query.all()
    users=User.query.all()
    return render_template('admin_search.html',scores=scores,users=users,chapters=chapters,quizes=quizes,questions=questions,subjects=subjects)

#Again Users Part
@app.route('/user_dash/<int:id>',methods=['POST','GET'])
def user_dash(id):
    user=User.query.filter_by(id=id).first()
    quizes=Quiz.query.all()  
    
    return render_template('user_dash.html',user=user,quizes=quizes)

@app.route('/user_dash/search/<int:id>',methods=['POST','GET'])
def user_search(id):
    user=User.query.filter_by(id=id).first()
    subjects=Subject.query.all()
    chapters=Chapter.query.all()
    quizes=Quiz.query.all()
    questions=Question.query.all()
    scores=Scores.query.all()
    return render_template('user_search.html',scores=scores,user=user,chapters=chapters,quizes=quizes,questions=questions,subjects=subjects)

@app.route('/user_dash/summary/<int:id>',methods=['POST','GET'])
def user_summary(id):
    user=User.query.filter_by(id=id).first()
    scores=Scores.query.filter_by(user_id=id).all()
    quizes=[]
    chapters=[]
    subjects=[]
    for s in scores:
        quiz=Quiz.query.filter_by(id=s.quiz_id).all()
        for q in quiz:
            quizes.append(q)
    for quiz in quizes:
        chapter=Chapter.query.filter_by(id=quiz.chapter_id).all()
        for c in chapter:
            chapters.append(c)
    for chapter in chapters:
        subject=Subject.query.filter_by(id=chapter.sub_id).all()
        for s in subject:
            subjects.append(s)
    
    return render_template('user_summary.html',scores=scores,user=user,chapters=chapters,subjects=subjects,quizes=quizes)

@app.route('/user_dash/score/<int:id>',methods=['POST','GET'])
def user_score(id):
    user=User.query.filter_by(id=id).first()
    scores=Scores.query.filter_by(user_id=id).all()
    quizes=Quiz.query.all() 
    return render_template('user_score.html',scores=scores,user=user,quizes=quizes)

@app.route('/user_dash/quiz_view/<int:user_id>/<int:quiz_id>')
def user_quiz_view(user_id,quiz_id):
    user=User.query.filter_by(id=user_id).first()
    quiz=Quiz.query.filter_by(id=quiz_id).first()
    if quiz:
        chapter=Chapter.query.filter_by(id=quiz.chapter_id).first()
        if chapter:
            subject=Subject.query.filter_by(id=chapter.sub_id).first()
        else:
            return "Chapter not found"
    else:
        return "Quiz not found"
    return render_template('user_quiz_view.html',quiz=quiz,chapter=chapter,subject=subject,user=user)

@app.route('/user_dash/quiz_attempt/<int:user_id>/<int:quiz_id>',methods=['POST','GET'])
def user_quiz_attempt(user_id,quiz_id):
    user=User.query.filter_by(id=user_id).first()
    quiz=Quiz.query.filter_by(id=quiz_id).first()
    questions=Question.query.filter_by(quiz_id=quiz_id).all()
    if request.method=='POST':
        score=0
        for que in questions:
            if que.ans==request.form[str(que.id)]:
                score+=1
        
        time_stamp=datetime.now()
        score=Scores(user_id=user_id,quiz_id=quiz_id,time_stamp=time_stamp,total_scored=score)
        db.session.add(score)
        db.session.commit()
        return redirect('/user_dash/'+str(user_id))
    return render_template('user_quiz_attempt.html',quiz=quiz,questions=questions,user=user)






#Running the flask app





if __name__ == '__main__':
    app.run(debug=True)