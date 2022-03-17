from flask import Flask, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired

import requests

from inventoryservice.db import Base, engine

r = requests.get(url=' http://131.155.205.108:5005/menutest')
menu = r.json()
options = []
for item in menu['order']:
    options.append((item['id'], f"{item['name']}: €{item['price']}"))
print(options)

