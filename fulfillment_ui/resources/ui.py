import os
import requests
from datetime import datetime
import json
import logging

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, HiddenField
from flask_bootstrap import Bootstrap


logging.basicConfig(level=logging.INFO)


class FulfillmentForm(FlaskForm):
    # FlaskWTF form class.
    fulfilled = BooleanField("Fulfilled")
    request = requests.get(url='http://api_gateway_ct:8081/unfulfilled_order').json()

    # Track order_id as hidden field.
    id = HiddenField()
    submit_order = SubmitField('Fulfill order')


def get_unfulfilled():
    form = FulfillmentForm()

    #logging.info(f"Hoi hoi hier is de request {r.json()}.")
    #r2 = json.loads(r.data.decode("utf-8"))
    #logging.info(f"Hoi hoi hier is de request {r2}.")
    message = "No unfulfilled orders."

    unfulfilled = form.request
    order_id = 0
    try:
        order_id = unfulfilled["order_id"]
        unfulfilled = unfulfilled['order_content']
        no_orders = False
    except KeyError:
        no_orders = True
    forms = []
    info = []
    """{'order_content': {'1': {'product_name': 'TEST', 'product_price': 1.5, 'quantity': 2},
                       '2': {'product_name': 'Leffe Blond', 'product_price': 2.5, 'quantity': 2}},
     'order_info': {'revenue': 4.5}}"""

    form.id.data = order_id
    forms.append(form)
    products = []
    # For order in ...
    if not no_orders:
        for key in unfulfilled.keys():
            try:
                product = unfulfilled[key]
                product_name = product["product_name"]
                product_quantity = product["order_quantity"]
                products.append(f"{product_name} x {product_quantity}")
                info.append([f"ID: {order_id}", products])
            except Exception as ex:
                print(ex)
    for form in forms:
        if form.validate_on_submit():
            # Boolean field for fulfillment (checkmark).
            data = form.fulfilled.data
            if data:
                order_id = form.id.data
                print(form.id.data, data)
                message = f"Fulfillment processed for order: {order_id}"
                requests.post(url="http://api_gateway_ct:8081/fulfilled_order", data=json.dumps({"order_id": order_id}))
    return info, message, forms


def fulfill(form, data):
    order_id = form.id.data
    print(form.id.data, data)
    message = f"Fulfillment processed for order: {order_id}"
    requests.post(url="http://api_gateway_ct:8081/fulfilled_order", data=json.dumps({"order_id": order_id}))
    return message
