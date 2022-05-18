from flask import jsonify
import random




class Payment:
    @staticmethod
    def bank_request(amount):
        # accept payment if below 30. If above, client lacks te funds to pay for order.
        amount = int(amount)
        if amount < 30:
            return jsonify({"output": f"payment of {amount} successful"}), 200
        else:
            return jsonify({"output": f"payment of {amount} was not successful"}), 500
