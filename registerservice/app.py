import random
import sqlite3
import datetime as dt
import logging
from dateutil.parser import parse
import pandas as pd

import requests

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap



from inventoryservice.db import Base, engine

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)
bootstrap = Bootstrap(app)


import os
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class OrderForm(FlaskForm):
    r = requests.get(url=' http://131.155.205.108:5005/menutest')
    menu = r.json()
    options = []
    for item in menu['order']:
        options.append(f"{item['name']}: €{item['price']}")
    #date_picker = DateField('DatePicker', format='%Y-%m-%d')
    product = SelectField(
        'product:',
        choices=options)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')

@app.route('/order', methods=['POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    message = ""

    if form.validate_on_submit():
        if form.submit_order.data:
            quantitty = form.quantity.data
            product = form.time_type.data

            form.place_number.data = ""
            # redirect the browser to another route and template
            message = "Order sent!"


    return render_template('index.html', form=form, message=message)



app.run(host='0.0.0.0', port=5003)
