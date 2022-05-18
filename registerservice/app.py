import os
import requests
import json
import logging
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap

from resources.ui import OrderForm, proces_order


app = Flask(__name__)
app.config["DEBUG"] = True
logging.basicConfig(level=logging.INFO)
# Initialize Flask Bootstrap for WTForm.
bootstrap = Bootstrap(app)

# Generate CSRF token for form.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def index():
    form = OrderForm()
    # Retrieve menu from class to avoid duplicate requests.
    menu = OrderForm.menu
    logging.info(menu)
    # Message will be shown to the user. Initially empty.
    message = ""
    if form.validate_on_submit():
        if form.submit_order.data:
            message = proces_order(form, menu)
    return render_template('index.html', form=form, message=message)
  
app.run(host='0.0.0.0', port=5000)
