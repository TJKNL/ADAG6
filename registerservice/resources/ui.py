import os
import requests
import json

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


class OrderForm(FlaskForm):
    # Class necessary for the fulfillment form (FlaskWTF).
    # Request products which are in stock.
    # TODO: replace url with actual menu service. Assignment 2
    r = requests.get(url=' http://api_gateway_ct:8081/GetMenu')
    menu = r.json()
    options = []
    # Options are stored as (id, options_text). when products.data is retrieved, only id is returned.
    print(menu)
    for key in menu.keys():
        for item in menu[key]:
            options.append((key, f"{item['product_name']}: €{item['product_price']}"))
    # TODO: Create multiple forms for multiple products per order.
    # SelectField is a dropdown with possible options.
    product = SelectField(
        'product:',
        choices=options)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')


def proces_order(form, menu):
    order = {}
    quantity = form.quantity.data
    product_id = form.product.data
    # Check if requested quantity is within inventory limits.
    if quantity > menu[product_id]['quantity']:
        message = f"We are sorry, the ordered amount of {menu[product_id]['name']} is unavailable."
        return render_template('index.html', form=form, message=message)
    # Calculate order total price.
    revenue = quantity * menu[product_id]['price']
    # Give user feedback.
    message = f"Your order has been sent. Order total: €{revenue}"
    # Generate order JSON for subsequent services.
    order_content = {}
    for i in range(0, 1):
        order_content[product_id] = {
            "product_name": menu[product_id]['name'],
            "product_price": menu[product_id]['price'],
            "quantity": menu[product_id]['quantity']
        }

    order = {
        "order_info": {
            "revenue": revenue,
        },
        "order_content": order_content
    }

    requests.post(url=f"http://api_gateway_ct:8080/NewOrder/{revenue}", json=json.dumps(order))
    print(order)  # Print order for demo purposes.
    return message
