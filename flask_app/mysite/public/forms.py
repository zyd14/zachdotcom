import datetime as dt
from functools import partial

import pytz
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, AnyOf


class PlantCount(FlaskForm):
    plant_type = StringField('Family of plant', validators=[DataRequired()])
    species = StringField('Plant species', validators=[DataRequired()])
    count = IntegerField('Number of plants', validators=[DataRequired()])
    location = StringField('Indoor / Outdoor', default='Indoor', validators=[partial(AnyOf, ['Indoor', 'Outdoor'])])
    date_started = DateField(default=dt.datetime.now(tz=pytz.timezone('UTC')))
    date_updated = DateField(default=dt.datetime.now(tz=pytz.timezone('UTC')))
    storage_method = StringField('How seeds were stored', default='Store',
                                 validators=[partial(AnyOf, ['Saved', 'Store'])])
    germinated = IntegerField('Total number germinated', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


class BlogEntry(FlaskForm):
    author = StringField('Post Author', validators=[DataRequired()])
    title = StringField('Post title', validators=[DataRequired()])
    content = StringField("What'd you do today?", validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.date.data:
            self.date.data = dt.datetime.today()