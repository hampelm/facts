# Capybara Facts!
# To load environment variables:
# os.environ['twilio_account'], os.environ['twilio_token']

import os

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    last_fact = db.Column(db.Integer)

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.last_fact = 0

    def __repr__(self):
        return '<Phone %r>' % self.phone


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.String(256))
    fact_number = db.Column(db.Integer)

    def __init__(self, fact, fact_number):
        self.fact = fact
        self.fact_number = fact_number

    def __repr__(self):
        return '<Fact %r>' % self.fact


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URL']
db = SQLAlchemy(app)

@app.route("/")
def hello():
    return "Hello World!"


if __name__ == "__main__":
    app.run()


# Database structure
	# Facts
		# Fact number
		# Fact
	# People
		# Phone number
		# Last fact number

# On request
	# Get list of facts
	# If current fact exists
	# Get list of numbers
	# For each numbers
		# Send the facts


# On message in 
	# If message from Matt
		# Broadcast message
	# Else
		# Send Matt the message
		

