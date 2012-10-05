# Capybara Facts!
# To load environment variables:
# os.environ['twilio_account'], os.environ['twilio_token']

import os

from flask import Flask
from twilio.rest import TwilioRestClient

app = Flask(__name__)

@app.route("/")
def hello():

    return "Hello World!"


if __name__ == "__main__":
    app.run()


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
		

