from flask import Flask, request

from db import Base, engine
from resources.products import Products
from resources.inventory import Inventory

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

# Hele python vgm niet meer nodig
@app.route('/inventory/<d_id>/<order_quantity>', methods=['PUT'])
def reduce(d_id, order_quantity):
    return Inventory.reduce(d_id, order_quantity)


app.run(host='0.0.0.0', port=5000)
