#flask Script Signup - Second day eid = 12-8-2019
#step1
#! /usr/bin/env python3
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length

#step9
from flask_sqlalchemy import SQLAlchemy

#step15 - password security
from werkzeug.security import generate_password_hash, check_password_hash


#step16
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user




app = Flask(__name__)
app.config['SECRET_KEY'] = 'my_secret_key'
Bootstrap(app)
#step10
db = SQLAlchemy(app)

#step17
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


#step11 for create user in database
class USER(UserMixin, db.Model):  #ask about what is meaning db.model #before db.model only
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


#step18
@login_manager.user_loader
def load_user(user_id):
    return USER.query.get(int(user_id))



#step8 the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://///root/Documents/flaskscripts/signup/database.db'

#step3
class LoginForm(FlaskForm):

    username = StringField('username',validators=[InputRequired(), Length(min=4, max=15)])
    password = StringField('password',validators=[InputRequired(), Length(min=4, max=15)])
    remember = BooleanField('Remember Me')



#step5
class RegisterForm(FlaskForm):

    email = StringField('email', validators=[InputRequired(), Email(message='ivalid Email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(),Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(),Length(min=4, max=15)])


#step2
@app.route('/')
def index():
    return render_template('index.html')







#step 4 and login.html
@app.route('/login', methods=['GET','POST'])
def login():

    form = LoginForm()

    #step7 for check the input data
    if form.validate_on_submit():

        #step13
        user = USER.query.filter_by(username=form.username.data).first()

        if user:

            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.password.data) #step21 for work login afterv add direct to login in dashboard
            #if user.password == form.password.data: before add hash security

                return redirect(url_for('dashboard'))

        return '<h1>الاسم أو كلمة المرور خطأ</h1>'

        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>' include step 7 for check the data


    return render_template('login.html', form=form)










#step6 and signup.html
@app.route('/signup', methods=['GET','POST'])
def signup():

    form = RegisterForm()

    #step7
    if form.validate_on_submit():

        #step14 hashed oassword security
        hashed_password = generate_password_hash(form.password.data, method='sha256')

        #step12 access user in database
        new_user = USER(username=form.username.data, email=form.email.data, password=hashed_password)#before = form.password.data
        db.session.add(new_user)
        db.session.commit()


        return '<h1>  تم إنشاء الحساب  بنجاح يمكنك الرجوع الي صفحة تسجيل الدخول الﻵن </h1>'



        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>' INCLUDE STEP 7 FOR CHECK THE DATA

    return render_template('signup.html', form=form)














@app.route('/dashboard')
#step20
@login_required #if open dashboard page will redirect automatic to login page
def dashboard():
    return render_template('dashboard.html', name=current_user.username)



#step22 and final - logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)