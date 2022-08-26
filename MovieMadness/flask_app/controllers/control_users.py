from flask_app import app
from flask import render_template, redirect,session,request, flash
from flask_app.models.user import User
from flask_app.models.show import Show
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/register', methods=['POST'])
def register():
    if User.validate(request.form) ==False:
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data={
        'first_name':request.form['first_name'],
        'last_name':request.form['last_name'],
        'email':request.form['email'],
        'password':pw_hash
        }
    user_id=User.save(data)
    session['user_id']=user_id
    return redirect('/dashboard')

@app.route('/login', methods=['POST'])
def log_in():
    data={'email': request.form['email']}
    user = User.get_by_email(data)
    if not user:
        flash ("Invalid Email or Password")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash ("Invalid Email or Password")
        return redirect ('/')
    session['user_id']=user.id
    return redirect('/dashboard')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/dashboard')
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data), shows=Show.get_all(data))