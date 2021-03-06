import os
import requests
import json
import logging
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
    try:
        menu["message"]
        empty_menu = True
    except KeyError as ex:
        empty_menu = False
    if empty_menu:
        # Inventory is empty.
        pass
    else:
        for key in menu.keys():
            item = menu[key]
            options.append((key, f"{item['product_name']}: €{item['product_price']}"))

    # TODO: Create multiple forms for multiple products per order.
    # SelectField is a dropdown with possible options.
    product = SelectField(
        'product:',
        choices=options)
    order_quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')


def proces_order(form, menu):
    order = {}

    order_quantity = form.order_quantity.data
    product_id = form.product.data

    # Check if requested order_quantity is within inventory limits.
    if order_quantity > menu[product_id]['product_quantity']:
        m_content = menu[product_id]['product_name']
        message = f"We are sorry, the ordered amount of {m_content} is unavailable."
        return message
    # Calculate order total price.
    revenue = order_quantity * menu[product_id]['product_price']
    # Give user feedback.
    message = f"Your order has been sent. Order total: €{revenue}"
    # Generate order JSON for subsequent services.
    order_content = {}
    for i in range(0, 1):
        order_content[int(product_id)] = {
            "product_name": menu[product_id]["product_name"],
            "product_price": menu[product_id]["product_price"],
            "order_quantity": order_quantity
        }

    order = {
        "order_info": {
            "revenue": revenue,
        },
        "order_content": order_content
    }
    logging.info(order)
    requests.post(url=f"http://api_gateway_ct:8081/NewOrder/{revenue}", data=json.dumps(order))
    print(order)  # Print order for demo purposes.
    return message
