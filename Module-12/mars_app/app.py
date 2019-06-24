#Unit 12 Assigment - Mission to Mars
#Step 2 MongoDB and Flask Application
#@version 1.0
#@author Martha Meses

import pymongo
import scrape_mars
import os
# FLASK
from flask import Flask, render_template, redirect

# APP
app = Flask(__name__)

# ROUTES
# home route to render index.html template using data from Mongo
@app.route("/")
def homePage():
    # Find record of data from the mongo database
    # destination_data = mongo.db.collection.find_one()
    import pymongo
    conn = 'mongodb://localhost:27017/'
    client = pymongo.MongoClient(conn)
    #data base name
    db = client.mars_db
    mars = db.marsData.find_one()
    # Return template and data
    return render_template("index.html", data=mars)

# scrape route
@app.route("/scrape")
def scrape():
    # Run the scrape function
    result = scrape_mars.scrape_data()
    # Update Mongo database 
    import pymongo
    conn = 'mongodb://localhost:27017/'
    client = pymongo.MongoClient(conn)
    #data base name
    db = client.mars_db
    collection = db.marsData
    # collection.insert_one(result)
    # collection.insert_many(result)
    collection.update({}, result, upsert=True)
    # Redirect back to home page
    return redirect("/")

# APP RUNNING
if __name__ == '__main__':
    app.run(debug=True)