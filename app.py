"""
Flask Olx Like app sell spot
"""
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

class Product(db.Model):
    """
    Database class
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    productname = db.Column(db.String(50))
    price = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    mail = db.Column(db.String(50))
    number = db.Column(db.String(50))
    cat = db.Column(db.String(50))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))

        return '<h1>Invalid username or password</h1>'
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created! <a href="/login">Login</a></h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/h')
@login_required
def home():
    """
    home route
    """
    posts = Product.query.order_by(Product.date_posted.desc()).all()

    return render_template('home.html', posts=posts, name=current_user.username)


@app.route('/post/<int:post_id>')
@login_required
def post(post_id):
    """
    Post page route
    """
    post = Product.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/sell')
@login_required
def add():
    """
    sell page route
    """
    return render_template('sell.html', name=current_user.username)

@app.route('/addpost', methods=['POST'])
@login_required
def addpost():
    """
    sell function route
    """
    name = request.form['uname']
    productname = request.form['pname']
    price = request.form['pr']
    content = request.form['p-des']
    mail = request.form['u-mail']
    number = request.form['u-num']
    cat = request.form['cat']

    post = Product(name=name, productname=productname, price=price, content=content, mail=mail, number=number, cat=cat , date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('home'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    #IN PRODUCTION debug=False