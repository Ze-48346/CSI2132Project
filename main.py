from flask import Flask, render_template

from flask_sqlalchemy import SQLAlchemy

from module import *

from flask_bootstrap import Bootstrap

app = Flask(__name__)


class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://zyang137:123456@localhost/mydatabase'  # 这里改成自己本地的数据库用户和密码
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)
db = SQLAlchemy(app)
Bootstrap(app)


@app.route("/")
def index():
    return render_template('HomePage.html')


@app.route("/login")
def login_page():
    return render_template('Signin Template for Bootstrap.html')


@app.route("/patient")
def patient_page():
    return render_template('PatientUI.html')


@app.route("/receptionist")
def receptionist_page():
    return render_template('ReceptionistUI.html')


@app.route("/dentist")
def dentist_page():
    return render_template('DentistsUI.html')


@app.route("/signup")
def signup():
    return render_template('signup.html')


if __name__ == '__main__':
    # db.drop_all()

    app.run(debug=False)
