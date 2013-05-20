Facts
=====

Think [Cat Facts](http://www.reddit.com/r/funny/comments/owx3v/so_my_little_cousin_posted_on_fb_that_he_was/).

![Cat facts](http://i.imgur.com/rsQ93.png)

It's a small script to send a fact from a list of facts to friends. A sample list of capybara facts is enclosed.


Install
=======

This runs great on Heroku.

You'll need:
* A Twilio account 
* A Postgres database

You'll need to set environment variables with details for those services. You can use the example `setenv.sh` in the repo (obviously, use your own environment variables and run `source setenv.sh`).

Make sure to set your phone number, too! That way, when people text back at your cat facts app, you can 
seamlessly (and anonymously!) reply to them.

Then, install with these commands:

`virtualenv env --no-site-packages`

To create a virtualenv

`source env/bin/activate`

To use your virtual environment

`pip install -r requirements.txt`

To install the required python packages into the environment

Then, to get started, run

`python server.py`

That will set up the database with fairly logical tables. 

Next, add the facts and a target (or two) to the database. 

Hit the endpoint, `http://yourserveraddress/`, to send the first round of facts. Further rounds can be sent manually
by visiting that address, or you can set up cron or the Heroku scheduler. 


