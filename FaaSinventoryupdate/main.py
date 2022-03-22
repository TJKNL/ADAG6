from db import Base, engine
from resources.order import Order
from resources.content import Content


def create_order(request):
    from flask import abort
    if request.method == 'POST':
        Base.metadata.create_all(engine)
        request_json = request.get_json(silent=True)
        return Order.create(request_json)
    else:
        return abort(405)


def get_unfulfilled_orders(request):
    from flask import abort
    if request.method == 'GET':
        Base.metadata.create_all(engine)
        return Order.get_unfulfilled()
    else:
        return abort(405)


def update_order_status(request):
    from flask import abort
    if request.method == 'PUT':
        Base.metadata.create_all(engine)
        request_json = request.get_json(silent=True)
        return Order.update_status(request_json)
    else:
        return abort(405)

#
# def delete_delivery(request):
#     from flask import abort
#     if request.method == 'DELETE':
#         Base.metadata.create_all(engine)
#         request_args = request.args
#         d_id = request_args['d_id']
#         return Delivery.delete(d_id)
#     else:
#         return abort(405)

