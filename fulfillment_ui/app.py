import os
import requests
from datetime import datetime
import json

from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, HiddenField
from flask_bootstrap import Bootstrap


from resources.ui import FulfillmentForm, get_unfulfilled, fulfill

app = Flask(__name__)
app.config["DEBUG"] = True

# Initialize Flask Bootstrap for WTForm.
bootstrap = Bootstrap(app)

# Generate CSRF token for form.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/fulfillment_ui', methods=['GET', 'POST'])
def index():
    r = requests.get(url='http://api_gateway_ct:8081/unfulfilled_order')
    info, message, forms = get_unfulfilled(r)

    return render_template('index.html', message=message, forms=forms, info=info)


app.run(host='0.0.0.0', port=5000)
