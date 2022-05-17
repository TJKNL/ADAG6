from flask import jsonify
import random


class Payment:
    @staticmethod
    def bank_request(amount):
        # Generate a random number to simulate failed payments. This functions simulates the bank.
        if random.randint(0, 100) < 50:
            return jsonify({"output": f"payment of {amount} successful"}), 200
        else:
            return jsonify({"output": f"payment of {amount} was not successful"}), 500