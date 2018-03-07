from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mars

@app.route('/')
def index():
    print("Loading page")
    mars_facts = db.mars_facts.find_one()
    print(mars_facts)
    return render_template('index.html', mars_facts = mars_facts)

@app.route('/scrape')
def scrape():
    mars_facts_data = scrape_mars.scrape()
    mars_facts = db.mars_facts
    mars_facts.update({}, mars_facts_data, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__ == "__main__":
    app.run(debug=True)