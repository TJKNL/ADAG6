from resources.fulfillmentform import FulfillmentForm


from inventorydirectservice.db import Base, engine

app = Flask(__name__)
app.config["DEBUG"] = True
Base.metadata.create_all(engine)

@app.route('/fulfillment_ui', methods=['GET', 'POST'])
def index():
    return FulfillmentForm.index()
