import os
import requests
from datetime import datetime

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, BooleanField, HiddenField
from wtforms_components import read_only
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

from inventoryservice.db import Base, engine

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

bootstrap = Bootstrap(app)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class FulfillmentForm(FlaskForm):
    fulfilled = BooleanField("Fulfilled")
    id = HiddenField()
    submit_order = SubmitField('Fulfill order(s)')


@app.route('/fulfillment_ui', methods=['GET', 'POST'])
def index():
    # TODO: replace url with real order FAAS.
    r = requests.get(url=' http://localhost:5005/unfulfilled')

    message = ""
    unfulfilled = r.json()
    forms = []
    info = []
    # For order in ...
    for key in unfulfilled.keys():

        order_id = key
        form = FulfillmentForm(prefix=order_id)
        form.id.data = order_id
        forms.append(form)

        products = []
        for key2 in unfulfilled[key]["order_content"].keys():
            product = unfulfilled[key]["order_content"][key2]
            product_name = product["product_name"]
            product_quantity = product["quantity"]
            products.append(f"{product_name} x {product_quantity}")
        info.append([f"ID: {key}", products])

    for form in forms:
        if form.validate_on_submit():
            # Boolean field for fullfilment,
            data = form.fulfilled.data
            if data:
                order_id = form.id.data
                print(form.id.data, data)
                message = "Fulfillment processed!"

    # TODO: Call change status FAAS & call order processing.

    return render_template('index.html', message=message, forms=forms, info=info)


app.run(host='0.0.0.0', port=5003)
