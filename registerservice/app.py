import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap

from resources.orderform import OrderForm


app = Flask(__name__)
app.config["DEBUG"] = True

# Initialize Flask Bootstrap for WTForm.
bootstrap = Bootstrap(app)

# Generate CSRF token for form.
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', form=form, message=message)

app.run(host='0.0.0.0', port=5003)
