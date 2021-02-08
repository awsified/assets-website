from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

app = Flask(__name__)

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
    

@app.route('/')
def index():
    machines = Asset.query.with_entities(Asset.machine).distinct()
    return render_template('index.html', machines=machines)


@app.route('/full/<machine>')
def full(machine):
    try:
        machines = Asset.query.filter_by(machine=machine).order_by(Asset.serial).all()
        return render_template('list.html', machines=machines, machine=machine)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


if __name__ == '__main__':
    app.run(debug=True)