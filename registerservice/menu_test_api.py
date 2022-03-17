from flask import Flask, request

from inventoryservice.db import Base, engine
#from resources.inventory import Inventory

import json

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


@app.route('/menutest', methods=['GET'])
def create_delivery():
    item1 = {'id': 3, 'name': 'Heiniken', 'price': 1.5, 'quantity': 10}
    item2 = {'id': 2, 'name': 'Pilsie', 'price': 3, 'quantity': 3}
    return json.dumps({'order': [item1, item2]})


app.run(host='0.0.0.0', port=5005)
