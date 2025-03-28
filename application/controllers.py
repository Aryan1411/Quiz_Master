from flask import current_app as app
from flask import  request, jsonify, render_template, redirect
from app import db,User,Subject,Chapter,Quiz,Question,Scores
from jinja2 import Template
from datetime import datetime, date,time
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
        sname=request.form['sname'].lower()
        sdesc=request.form['sdesc'].lower()
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
        sname=request.form['sname'].lower()
        sdesc=request.form['sdesc'].lower()
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
        cname=request.form['cname'].lower()
        cdesc=request.form['cdesc'].lower()
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
        sname=request.form['cname'].lower()
        sdesc=request.form['cdesc'].lower()
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
@app.route('/admin_dash/search',methods=['GET'])
def admin_search():
    return render_template('admin_dash_search.html')
@app.route('/admin_dash/search_result',methods=['GET'])
def admin_search_result():
    key=request.args.get('type')
    value=request.args.get('search').strip().lower()
    if key=='Subject':
            result=Subject.query.filter_by(name=value).all()
    elif key=='Chapter':
            result=Chapter.query.filter_by(name=value).all()
    elif key=='Quiz':
            result=Quiz.query.filter_by(id=value).all()
    elif key=='User':
            result=User.query.filter_by(name=value).all()      
    return render_template('admin_dash_search_result.html',result=result,key=key)

#Again Users Part
@app.route('/user_dash/<int:id>',methods=['POST','GET'])
def user_dash(id):
    user=User.query.filter_by(id=id).first()
    quizes=Quiz.query.all()  
    
    return render_template('user_dash.html',user=user,quizes=quizes)

@app.route('/user_dash/search/<int:id>',methods=['GET'])
def user_search(id):
    user=User.query.filter_by(id=id).first()
    return render_template('user_search.html',user=user)

@app.route('/user_dash/search_result/<int:id>',methods=['GET'])
def user_search_result(id):
    user=User.query.filter_by(id=id).first()
    key=request.args.get('type')
    value=request.args.get('search').strip().lower()
    if key=='Subject':
            result=Subject.query.filter_by(name=value).all()
    elif key=='Chapter':
            result=Chapter.query.filter_by(name=value).all()
    elif key=='Quiz':
            result=Quiz.query.filter_by(id=value).all()

    return render_template('user_search_result.html',result=result,key=key,user=user)



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

