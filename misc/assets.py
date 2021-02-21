import models
from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


# from flask_wtf import FlaskForm
# from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField
# from wtforms.validators import InputRequired, Length, Regexp, NumberRange

app = Flask(__name__)

# Flask-WTF requires an enryption key - the string can be anything
app.config['SECRET_KEY'] = 'MLXH243GssUWwKdTWS7FDhdwYF56wPj8'

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



@app.route('/')
def index():
    machines = Asset.query.with_entities(Asset.machine).distinct()
    return render_template('index.html', machines=machines)

@app.route('/testform')
def test():
    form1 = SearchForm()
        if form1.validate_on_submit():
        machine = request.form['machine']
        employee = request.form['employee']
        tag = request.form['tag']
        serial = request.form['serial']
        mac = request.form['mac']
        location = request.form['location']
        # the data to be inserted into Asset model - the table, assets
        record = Asset(machine, employee, tag, serial, mac, location)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"The data for asset {machine} has been submitted."
        return render_template('add_record.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)

@app.route('/inventory/<machine>')
def inventory(machine):
    try:
        machines = Asset.query.filter_by(machine=machine).order_by(Asset.serial).all()
        return render_template('list_asset.html', machines=machines, machine=machine)
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text

# add a new item to the database
@app.route('/add_record', methods=['GET', 'POST'])
def add_record():
    form1 = AddRecord()
    if form1.validate_on_submit():
        machine = request.form['machine']
        employee = request.form['employee']
        tag = request.form['tag']
        serial = request.form['serial']
        mac = request.form['mac']
        location = request.form['location']
        # the data to be inserted into Asset model - the table, assets
        record = Asset(machine, employee, tag, serial, mac, location)
        # Flask-SQLAlchemy magic adds record to database
        db.session.add(record)
        db.session.commit()
        # create a message to send to the template
        message = f"The data for asset {machine} has been submitted."
        return render_template('add_record.html', message=message)
    else:
        # show validaton errors
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('add_record.html', form1=form1)


@app.route('/search_assets/', methods=['GET', 'POST'])
def search_assets():
    #form3 = SearchForm()
    searchbar = request.form.get('searchbar',0)
    assets = Asset.query.filter(Asset.machine.contains(searchbar)).all()
    return render_template('search_assets.html', assets=assets)

@app.route('/select_record/<letters>')
def select_record(letters):
    # alphabetical lists by sock name, chunked by letters between _ and _
    # .between() evaluates first letter of a string
    a, b = list(letters)
    assets = Asset.query.filter(Asset.employee.between(a, b)).order_by(Asset.employee).all()
    return render_template('select_record.html', assets=assets)

# edit or delete - come here from form in /select_record
@app.route('/edit_or_delete', methods=['POST'])
def edit_or_delete():
    id = request.form['id']
    choice = request.form['choice']
    asset = Asset.query.filter(Asset.machine == id).first()
    # two forms in this template
    form1 = AddRecord()
    form2 = DeleteForm()
    return render_template('edit_or_delete.html', asset=asset, form1=form1, form2=form2, choice=choice)

# result of delete - this function deletes the record
@app.route('/delete_result', methods=['POST'])
def delete_result():
    id = request.form['id_field']
    purpose = request.form['purpose']
    asset = Asset.query.filter(Asset.machine == id).first()
    if purpose == 'delete':
        db.session.delete(asset)
        db.session.commit()
        message = f"The asset {asset.machine} has been deleted from the database."
        return render_template('result.html', message=message)
    else:
        # this calls an error handler
        abort(405)

# result of edit - this function updates the record
@app.route('/edit_result', methods=['POST'])
def edit_result():
    machine = request.form['id_field']
    # call up the record from the database
    asset = Asset.query.filter(Asset.machine == machine).first()
    # update all values
    asset.machine = request.form['machine']
    asset.employee = request.form['employee']
    asset.tag = request.form['tag']
    asset.serial = request.form['serial']
    asset.mac = request.form['mac']
    asset.location = request.form['location']

    form1 = AddRecord()
    if form1.validate_on_submit():
        # update database record
        db.session.commit()
        # create a message to send to the template
        message = f"The data for asset {asset.machine} has been updated."
        return render_template('result.html', message=message)
    else:
        # show validaton errors
        asset.machine = machine
        # see https://pythonprogramming.net/flash-flask-tutorial/
        for field, errors in form1.errors.items():
            for error in errors:
                flash("Error in {}: {}".format(
                    getattr(form1, field).label.text,
                    error
                ), 'error')
        return render_template('edit_or_delete.html', form1=form1, asset=asset, choice='edit')



if __name__ == '__main__':
    app.run(debug=True)