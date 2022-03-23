# BarGood
## Advanced Data Architectures - Group 6

This Github repositrie stores the BarGood bar service system. 

This system, comprised of mulitple microservices and FaaS components, serves to create more efficient ordering system for a beverage only bar. This is achieved by giving the customers their own ordering UI with which orders can be created, payed and sent to the bar personell. 

### Technical aspects
Each microservice can be run seperately as a independent Flask application. 
Google Cloud Fucntions is used for the three FaaS functions which are implemented to relief computational stress from the systems hosting the UI.

### Testing
Each service can be run by executing the app.py file in the respective service directories.

### Notes
In a future release this application will be using Docker but this is not yet implemented.
