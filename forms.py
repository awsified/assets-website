from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField
from wtforms.validators import InputRequired, Length, Regexp, NumberRange

class AddRecord(FlaskForm):
    # id used only by update/edit
    id_field = HiddenField()
    machine = StringField('Enter machine name', [ InputRequired(), Regexp(r'^[A-Za-z0-9\s\-\']+$', message="Invalid machine name")])
    employee = StringField('Enter employee name', [ InputRequired(), Regexp(r'^[A-Z][A-Za-z0\s\-\']+$', message="Invalid employee name (Make sure the first letter is capitalized)")])
    tag = StringField('IIA tag')
    serial = StringField('HP serial tag')
    mac = StringField('MAC Address')
    location = StringField('Location')
    
    submit = SubmitField('Add/Update Record')

class SearchForm(FlaskForm):
    search_string = StringField('Enter a machine to search for:', [ InputRequired(), Regexp(r'^[A-Za-z0-9\s\-\']+$', message="Invalid machine name")])

    submit = SubmitField('Search')

class DeleteForm(FlaskForm):
    id_field = HiddenField()
    purpose = HiddenField()
    submit = SubmitField('Delete This Asset')