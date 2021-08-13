from flask_wtf import FlaskForm
from wtforms.fields import StringField
from wtforms.validators import InputRequired, DataRequired, Optional
# from wtforms.fields.html5 import DateField
# from datetime import datetime


class searchCluster(FlaskForm):
    search_cluster = StringField(label="", 
        render_kw={'placeholder':'Cluster Name, State, or District', 'class':'form-control mr-sm-2', 'aria-label': 'Search'}, 
        default=None, validators=[InputRequired()]
    )
    # state = SelectField('State', coerce=str, default=0, validators=[Optional()])
    # district = StringField('District', render_kw={'placeholder': 'Example: Kota Kinabalu'}, validators=[Optional()])
    # date =  DateField('Date Announced', validators=[Optional()], format='%Y-%m-%d')
    # status = SelectField('Status', choices=[('0', 'All'),('active', 'Active'), ('ended', 'Ended')], default=0, validators=[Optional()])
    # category = SelectField('Category', coerce=str, default=0, validators=[Optional()])
    # deaths = IntegerField('Total Death(s)', default=0, validators=[Optional()])
    # recovered = IntegerField('Total recovered', default=0, validators=[Optional()])
    # submit = SubmitField('Submit')