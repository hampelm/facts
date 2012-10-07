# Capybara Facts!
# To load environment variables:
# os.environ['TWILIO_ACCOUNT'], os.environ['TWILIO_TOKEN']

import datetime
import os

from flask import Flask
from flask import request
from flask.ext.sqlalchemy import SQLAlchemy
from twilio.rest import TwilioRestClient

# Set up the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['POSTGRES_URL']
db = SQLAlchemy(app)
client = TwilioRestClient(os.environ['TWILIO_ACCOUNT'], 
    os.environ['TWILIO_TOKEN'])

# Set up the simple state tracking we need: people and facts.
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    phone = db.Column(db.String(15))
    next_fact = db.Column(db.Integer)
    last_message_datetime = db.Column(db.DateTime(timezone=False))

    def __init__(self, name, phone):
        self.name = name
        self.phone = phone
        self.last_fact = 0

    def __repr__(self):
        return '<Phone %r>' % self.phone


class Fact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fact = db.Column(db.String(160))
    fact_number = db.Column(db.Integer)

    def __init__(self, fact, fact_number):
        self.fact = fact
        self.fact_number = fact_number

    def __repr__(self):
        return '<Fact %r>' % self.fact


# Create the tables if needed 
db.create_all()


# Send out some facts!!
@app.route("/")
def hello():
    facts = Fact.query.order_by(Fact.fact_number).all()
    number_of_facts = len(facts)
    people = Person.query.all()

    for person in people:
        print person.next_fact
        print number_of_facts

        # If there is another fact for this person, send it to them
        # Otherwise, dont do anything.
        if person.next_fact < number_of_facts:          
            fact_to_send = facts[person.next_fact].fact

            # Send the fact
            message = client.sms.messages.create(to=person.phone, from_=os.environ['TWILIO_NUMBER'],
                                                    body=fact_to_send)

            # Update the database
            person.next_fact = person.next_fact + 1
            db.session.add(person)
            db.session.commit()


    return "Capybaras for life!"

@app.route('/twilio', methods=['POST'])
def incoming():
    if request.method == 'POST':
        from_phone = request.form['From']
        body = request.form['Body']

        if from_phone == os.environ['MY_NUMBER']:
            # If the message is from the admin, we need to find out 
            # who to send it on to.

            target = Person.query.filter(Person.last_message_datetime != None).order_by(Person.last_message_datetime.desc()).first()
            print target.phone
            print target.name

            if target is not None:
                print "Forwarding message FROM the admin"
                message = client.sms.messages.create(to=target.phone, 
                    from_=os.environ['TWILIO_NUMBER'], body = body)

        else:
            # Set this person as the origin of the most recent message
            from_person = Person.query.filter(Person.phone == from_phone).first()
            print from_person.name 
            from_person.last_message_datetime = datetime.datetime.now()
            db.session.add(from_person)
            db.session.commit()

            print from_person.last_message_datetime
            print from_person.name

            # Forward the message to the admin
            print "Forwarding message TO the admin"
            message = client.sms.messages.create(to=os.environ['MY_NUMBER'], 
                from_=os.environ['TWILIO_NUMBER'], body=body)


    return ""


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
