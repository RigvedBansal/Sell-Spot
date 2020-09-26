from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

Flask = (__name__)

@app.route('/')
def home():
    return "Test"

if __name__ == "__main__":
    app.run(debug=True)