# Importing the required libraries
from flask import Flask
from application.database import db

#Initialising the flask app
app=Flask(__name__)



#Configuring the database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
app.app_context().push()

from application.models import *
from application.controllers import *
#Initialising the database

#db.create_all() 
#Running the flask app

if __name__ == '__main__':
    app.run(debug=True)