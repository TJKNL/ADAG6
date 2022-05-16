from resources.fulfillmentform import Fullfillmentform


@app.route('/fulfillment_ui', methods=['GET', 'POST'])
def index():
    return Fullfillmentform.index()
