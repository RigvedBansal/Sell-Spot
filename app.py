from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    productname = db.Column(db.String(50))
    price = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    mail = db.Column(db.String(50))
    number = db.Column(db.String(50))
    cat = db.Column(db.String(50))

@app.route('/')
def index():
    posts = Product.query.order_by(Product.date_posted.desc()).all()

    return render_template('index.html', posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    post = Product.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/sell')
def add():
    return render_template('sell.html')

@app.route('/addpost', methods=['POST'])
def addpost():
    username = request.form['uname']
    productname = request.form['pname']
    price = request.form['pr']
    content = request.form['p-des']
    mail = request.form['u-mail']
    number = request.form['u-num']
    cat = request.form['cat']

    post = Product(username=username, productname=productname, price=price, content=content, mail=mail, number=number, cat=cat , date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)