import os
from .routes import *
from .forms import SearchForm, DeleteForm, AddRecord
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

Bootstrap(app)

db_name = 'assets.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)

class Asset(db.Model):
    __tablename__ = 'asset-list'
    machine = db.Column(db.String, primary_key=True)
    employee = db.Column(db.String)
    tag = db.Column(db.String)
    serial = db.Column(db.String)
    mac = db.Column(db.String)
    location = db.Column(db.String)

    def __init__(self, machine, employee, tag, serial, mac, location):
        self.machine = machine
        self.employee = employee
        self.tag = tag
        self.serial = serial
        self.mac = mac
        self.location = location