from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'

db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    p_name = db.Column(db.String(50))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    cat = db.Column(db.String(20))
    price = db.Column(db.String(20))
    mail = db.Column(db.String(50))
    number = db.Column(db.Integer)

@app.route('/')
def index():
    posts = Product.query.order_by(Product.date_posted.desc()).all()

    return render_template("index.html", posts=posts)

@app.route('/sell')
def sell():
    return render_template("sell.html")

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Product.query.filter_by(id=post_id).one()

    return render_template('post.html', post=post)

@app.route('/addpost', methods=['POST', 'GET'])
def addpost():
    name = request.form['u-name']
    p_name = request.form['p-name']
    content = request.form['p-des']
    cat = request.form['cat']
    pri = request.form['pr']
    cur = request.form['cur']
    price = cur + pri
    mail = request.form['u-mail']
    number = request.form['u-num']
    if number == "" or number == " ":
        number = None
    else:
        number = number

    post = Product(name=name, p_name=p_name, content=content, cat=cat, price=price, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)