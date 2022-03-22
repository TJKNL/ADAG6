from flask import Flask

from inventoryservice.db import Base, engine
# from resources.inventory import Inventory
from datetime import datetime
import json

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


# This function mimics the get_unfulfilled FAAS in Gcloud Functions.
@app.route('/unfulfilled', methods=['GET'])
def create_unfulfilled():
    order = {
        '7': {
            'order_info': {
                'revenue': 4.5, 'status': 'UNFULFILLED',
                'timestamp': str(datetime.now())
            },
            'order_content': {
                '3': {
                    'product_name': 'Heiniken', 'product_price': 1.5, 'quantity': 10
                },
                '6': {
                    'product_name': 'Jup', 'product_price': 2.5, 'quantity': 50
                }
            }
        },
        '10': {
            'order_info': {
                'revenue': 4.5, 'status': 'UNFULFILLED',
                'timestamp': str(datetime.now())
            },
            'order_content': {
                '7': {
                    'product_name': 'Leffe', 'product_price': 1.5, 'quantity': 2
                },
                '8': {
                    'product_name': 'Hein', 'product_price': 2.5, 'quantity': 3
                }
            }
        }
    }
    return json.dumps(order)


app.run(host='0.0.0.0', port=5005)
