from flask import Flask, request
import logging

from db import Base, engine
from resources.order import Order

# basic setup
app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

logging.basicConfig(level=logging.INFO)

@app.route('/order', methods=['POST'])
def create_order():
    req_data = request.get_json()
    return Order.create(req_data)


@app.route('/order/unfulfilled', methods=['GET'])
def get_unfulfilled_orders():
    return Order.get_unfulfilled()

@app.route('/order/<d_id>/<status>', methods=['PUT'])
def update_order_status():
    req_data = request.get_json()
    return Order.update_status(req_data)


app.run(host='0.0.0.0', port=5000)
