from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

import requests

from inventoryservice.db import Base, engine

class OrderForm(FlaskForm):



    r = requests.get(url=' http://localhost:5005/menutest')
    menu = r.json()
    options = []
    for item in menu['menu']:
        options.append(f"{item['name']}: €{item['price']}")
    product = SelectField(
        'product:',
        choices=options)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')



form = OrderForm()
print(form.menu)