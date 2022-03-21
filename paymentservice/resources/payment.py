from flask import jsonify
import json
from datetime import datetime
import random


class Payment:
    @staticmethod
    def bank_request(amount):
        if random.randint(0, 100) < 95:
            return jsonify({"output": f"payment of {amount} successful"}), 200
        else:
            return jsonify({"output": f"payment of {amount} was not successful"}), 500
