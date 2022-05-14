from flask import Flask
from resources.payment import Payment

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/payment/<amount>', methods=['GET'])
def bank_request(amount):
    return Payment.bank_request(amount)


app.run(host='0.0.0.0', port=5000)
