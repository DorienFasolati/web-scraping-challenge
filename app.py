from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pymongo
import requests
import mars_scrape

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
# client = pymongo.MongoClient('mongodb://localhost:27017/')
# db = client.mars
# mars_data = db.mars_data

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client.mars
collection = db.mars_data
db.collection.drop()

# Or set inline
# mongo = PyMongo(app, uri="mongodb://localhost:27017/craigslist_app")


@app.route("/")
def home():
    mars_data = list(db.collection.find())
    return render_template("index.html", mars_data = mars_data)


@app.route("/scraper")
def scraper():   
    mars_scrape_data = mars_scrape.scrape()
    db.collection.replace_one({}, mars_scrape_data, upsert=True)
    return redirect('/')
    


if __name__ == "__main__":
    app.run(debug=True)
