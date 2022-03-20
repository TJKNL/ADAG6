import os
import requests
from datetime import datetime

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



SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class OrderForm(FlaskForm):
    # TODO: replace url with real menu service.
    r = requests.get(url=' http://localhost:5005/menutest')
    menu = r.json()
    print(menu)
    options = []
    # Options are stored as (id, options_text). when products.data is retrieved, only id is returned.
    for key in menu.keys():
        item = menu[key]
        print(item)
        options.append((key, f"{item['name']}: €{item['price']}"))

    product = SelectField(
        'product:',
        choices=options)
    quantity = IntegerField('Quantity:', validators=[DataRequired()])
    submit_order = SubmitField('Place Order')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    # Retrieve menu from class to avoid duplicate requests.
    menu = OrderForm.menu
    message = ""
    order = {}

    if form.validate_on_submit():
        if form.submit_order.data:
            quantity = form.quantity.data
            product_id = form.product.data
            if quantity > menu[product_id]['quantity']:
                message = f"We are sorry, the ordered amount of {menu[product_id]['name']} is unavailable."
                return render_template('index.html', form=form, message=message)

            revenue = quantity * menu[product_id]['price']
            # Give user feedback
            message = f"Your order has been sent. Order total: €{revenue}"

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
                    "status": "UNFULFILLED",
                    "timestamp": datetime.now()
                },
                "order_content": order_content
            }

    # TODO: Check payment.

    # TODO: Send order.

    return render_template('index.html', form=form, message=message)


app.run(host='0.0.0.0', port=5003)
