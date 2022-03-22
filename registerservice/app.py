import os
import requests

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config["DEBUG"] = True


bootstrap = Bootstrap(app)

# Generate CSRF token for form.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


class OrderForm(FlaskForm):
    # Class necessary for the fulfillment form (FlaskWTF).
    # Request products which are in stock.
    # TODO: replace url with actual menu service. Assignment 2
    r = requests.get(url=' http://localhost:5005/menutest')
    menu = r.json()
    options = []
    # Options are stored as (id, options_text). when products.data is retrieved, only id is returned.
    for key in menu.keys():
        item = menu[key]
        options.append((key, f"{item['name']}: €{item['price']}"))
    # TODO: Create multiple forms for multiple products per order.
    # SelectField is a dropdown with possible options.
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
    # Message will be shown to the user. Initially empty.
    message = ""
    order = {}

    if form.validate_on_submit():
        if form.submit_order.data:
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

    # TODO: Check payment with payment service. Assignment 2

    # TODO: Send order. Assignment 2

    return render_template('index.html', form=form, message=message)

  
app.run(host='0.0.0.0', port=5003)
