from flask import Flask, request

from inventoryservice.db import Base, engine
from resources.products import Products
from resources.inventory import Inventory

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/products', methods=['POST'])
def create_product():
    req_data = request.get_json()
    return Products.create(req_data)


@app.route('/inventory', methods=['POST'])
def create_inventory():
    req_data = request.get_json()
    return Inventory.create(req_data)


@app.route('/inventory/<d_id>', methods=['GET'])
def get_inventory(d_id):
    return Inventory.get(d_id)


@app.route('/inventory/menu/', methods=['GET'])
def get_nonzero():
    return Inventory.get_nonzero()


@app.route('/inventory/<d_id>', methods=['DELETE'])
def delete_inventory_item(d_id):
    return Inventory.delete(d_id)


@app.route('/products/<d_id>', methods=['DELETE'])
def delete_products_item(d_id):
    return Products.delete(d_id)


@app.route('/inventory/menu', methods=['GET'])
def get_menu():
    return Inventory.get_nonzero()


@app.route('/inventory/<d_id>/<order_quantity>', methods=['PUT'])
def reduce(d_id=0, order_quantity=0):
    return Inventory.reduce(d_id, order_quantity)


app.run(host='0.0.0.0', port=5000)

