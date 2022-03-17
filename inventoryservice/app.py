from flask import Flask, request

from inventoryservice.db import Base, engine
from resources.products import Products
from resources.inventory import Inventory


app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/product', methods=['POST'])
def create_product():
    req_data = request.get_json()
    return Products.create(req_data)

@app.route('/inventory', methods=['POST'])
def create_inventory():
    req_data = request.get_json()
    return Inventory.create(req_data)

@app.route('/inventory/<d_id>', methods=['GET'])
def get_delivery(d_id):
    return Inventory.get(d_id)

@app.route('/inventory/<d_id>', methods=['DELETE'])
def delete_item(d_id):
    return Inventory.delete(d_id)

@app.route('/inventory/menu', methods=['GET'])
def get_menu():
    return Inventory.get_nonzero()

app.run(host='0.0.0.0', port=5003)
