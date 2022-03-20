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




@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()

    ## Ik kan niet de prijzen en id's uit het menu halen. dat is wat niet kan okee dopei

    # Retrieve menu from class to avoid duplicate requests.
    menu = OrderForm.menu
    message = ""
    print(menu)
    products = {}
    for item in menu:
        print(item)
        products[item.id] = item.price

    if form.validate_on_submit():
        if form.submit_order.data:
            quantity = form.quantity.data
            product_id = form.product.data
            print(menu)
            #total_price = quantity * menu['menu'].price[menu.id == product_id]

            # Give user feedback
            message = f"Order total: 10"


    return render_template('index.html', form=form, message=menu)


app.run(host='0.0.0.0', port=5003)
