from os import getenv
from flask import render_template, request, flash
from .assets import app, Asset, db
from .forms import AddRecord, DeleteForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app.config['SECRET_KEY'] = getenv('SECRET_KEY')

Bootstrap(app)

@app.route('/')
def index():
    assets = Asset.query.all()
    return render_template('index.html', assets=assets)


@app.route('/search_records', methods=['GET', 'POST'])
def search_records():
    searchterm = request.args.get('search')
    assets = Asset.query.filter(Asset.machine.contains(searchterm)).all()
    return render_template('search_records.html', assets=assets)

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