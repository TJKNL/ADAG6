from flask import Flask

from inventorydirectservice.db import Base, engine

import json

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)


# This file mimics the get_menu function of the inventory service for demo purposes.
@app.route('/menutest', methods=['GET'])
def create_delivery():
    item1 = {'name': 'Heiniken', 'price': 1.5, 'quantity': 10}
    item2 = {'name': 'Pilsie', 'price': 3, 'quantity': 3}
    item3 = {'name': 'Heineken', 'price': 20, 'quantity': 3}
    return json.dumps({'3': item1, '2': item2, '5': item3})


app.run(host='0.0.0.0', port=5005)
