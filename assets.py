from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

load_dotenv()

app = Flask(__name__)

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

from .routes import index, inventory, add_record,select_record,edit_or_delete,delete_result,search_records