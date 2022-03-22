from flask import Flask, request

from FaaSinventoryupdate.db import Base, engine
from resources.order import Order
from resources.content import Content

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/order', methods=['POST'])
def create_order():
    req_data = request.get_json()
    return Order.create(req_data)


@app.route('/order/<d_id>', methods=['GET'])
def get_unfulfilled_orders():
    return Order.get_unfulfilled()

@app.route('/order/<d_id>/status', methods=['PUT'])
def update_delivery_status(d_id):
    status = request.args.get('status')
    return Status.update(d_id, status)

#
# @app.route('/inventory', methods=['POST'])
# def create_inventory():
#     req_data = request.get_json()
#     return Inventory.create(req_data)
#
#
# @app.route('/inventory/<d_id>', methods=['GET'])
# def get_inventory(d_id):
#     return Inventory.get(d_id)
#
#
# @app.route('/inventory/menu/', methods=['GET'])
# def get_nonzero():
#     return Inventory.get_nonzero()
#
#
# @app.route('/inventory/<d_id>', methods=['DELETE'])
# def delete_inventory_item(d_id):
#     return Inventory.delete(d_id)
#
#
# @app.route('/products/<d_id>', methods=['DELETE'])
# def delete_products_item(d_id):
#     return Products.delete(d_id)

#
# @app.route('/inventory/menu', methods=['GET'])
# def get_menu():
#     return Inventory.get_nonzero()


app.run(host='0.0.0.0', port=5003)
