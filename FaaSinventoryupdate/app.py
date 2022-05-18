from flask import Flask, request

from db import Base, engine
from resources.order import Order
from resources.content import Content

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/order', methods=['POST'])
def create_order():
    req_data = request.get_json()
    return Order.create(req_data)


@app.route('/order/unfulfilled', methods=['GET'])
def get_unfulfilled_orders():
    return Order.get_unfulfilled()

@app.route('/order/<d_id>/<status>', methods=['PUT'])
def update_order_status(d_id, status):
    return Order.update_status(d_id, status)


app.run(host='0.0.0.0', port=5003)
