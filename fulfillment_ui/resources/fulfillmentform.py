# Complete copy paste van app

import os
import requests
from datetime import datetime

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, HiddenField
from flask_bootstrap import Bootstrap

from inventorydirectservice.db import Base, engine

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

# Initialize Flask Bootstrap for WTForm.
bootstrap = Bootstrap(app)

# Generate CSRF token for form.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class FulfillmentForm(FlaskForm):
    # FlaskWTF form class.
    fulfilled = BooleanField("Fulfilled")
    # Track order_id as hidden field.
    id = HiddenField()
    submit_order = SubmitField('Fulfill order')


@app.route('/fulfillment_ui', methods=['GET', 'POST'])
def index():
    # TODO: replace url with real order FAAS. Assignment 2
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
            # Boolean field for fulfillment (checkmark).
            data = form.fulfilled.data
            if data:
                order_id = form.id.data
                print(form.id.data, data)
                message = f"Fulfillment processed for order: {order_id}"

    # TODO: Call change status FAAS & call order processing. Assignment 2

    return render_template('index.html', message=message, forms=forms, info=info)


app.run(host='0.0.0.0', port=5000)
