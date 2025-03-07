import signal
import sys
from website import create_app
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

app = create_app()
db =SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///database.db'
app.config['SECRET_KEY']='thisisakey'



if __name__ == '__main__':
    app.run(debug=True)     #set it to False when run it in prodaction
