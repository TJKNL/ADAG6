from flask import Flask, request

from inventoryservice.db import Base, engine
from resources.inventory import Inventory

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

# Get menu
@app.route('/inventory/get_nonzero', methods=['GET'])
def get_menu():
    menu = request.get_json()
    return menu

# Get input
@app.route('/inventory/<d_id>', methods=['GET'])
def get_input(d_id):
    return Inventory.get(d_id)

# Check quantity, sum order?
@app.route('/inventory/<d_id>', methods=['GET']) #??
def check_quantity(d_id):
    return Inventory.delete(d_id)

# Get payment
@app.route('/inventory', methods=['GET'])
def get_payment():
    req_data = request.get_json()
    return Inventory.create(req_data)

# Get order processing
@app.route('/inventory/<d_id>', methods=['GET'])
def get_orderprocessing(d_id):
    return Inventory.get(d_id)



app.run(host='0.0.0.0', port=5003)
