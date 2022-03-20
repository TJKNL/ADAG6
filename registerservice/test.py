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
    # Options are stored as (id, options_text). when products.data is retrieved, only id is returned.
    for item in menu['menu']:
        options.append((item['id'], f"{item['name']}: €{item['price']}"))
    product = SelectField(
        'product:',
        choices=options)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')




#@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()

    ## Ik kan niet de prijzen en id's uit het menu halen. dat is wat niet kan okee dopei

    # Retrieve menu from class to avoid duplicate requests.
    menu = OrderForm.menu
    message = ""
    print(menu)
    products = {}
    for item in menu['menu']:
        print(item)
        products[item.id] = item.price

    return
index()