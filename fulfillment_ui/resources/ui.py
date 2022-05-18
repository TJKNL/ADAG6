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
    # Track order_id as hidden field.
    id = HiddenField()
    submit_order = SubmitField('Fulfill order')


def get_unfulfilled():
    r = requests.get(url='http://api_gateway_ct:8081/unfulfilled_order')
    logging.info(f"Hoi hoi hier is de request {r.get_json()}.")
    r2 = json.loads(r.data.decode("utf-8"))
    logging.info(f"Hoi hoi hier is de request {r2}.")
    message = ""
    unfulfilled = r.json()
    forms = []
    info = []
    # For order in ...
    print("unfulfilled output test:")
    print(unfulfilled)
    for key in unfulfilled.keys():

        order_id = key
        form = FulfillmentForm(prefix=order_id)
        form.id.data = order_id
        forms.append(form)

        products = []
        print(key)
        try:
            for key2 in unfulfilled[key]["order_content"].keys():
                product = unfulfilled[key]["order_content"][key2]
                product_name = product["product_name"]
                product_quantity = product["quantity"]
                products.append(f"{product_name} x {product_quantity}")
            info.append([f"ID: {key}", products])
        except Exception as ex:
            print(ex)
        return info, message, forms


def fulfill(form, data):
    order_id = form.id.data
    print(form.id.data, data)
    message = f"Fulfillment processed for order: {order_id}"
    requests.post(url="http://api_gateway_ct:8081/fulfilled_order", json=json.dumps({"order_id": order_id}))
    return message
