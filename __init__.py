import os
import imaplib
import email

from flask import Flask
from flask import render_template


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/')
    def hello():
        dicty = dictionary_creation()
        return render_template("index.html", sessions = dicty)
    return app

def dictionary_creation():
    emails = []
    people = []

    for email in get_emails():
        if is_email_valid(email["body"]):
            email["body"] = get_original_email(email["body"])
            email["date_time"] = get_date_time(email["body"])
            email["name"] = get_name(email["from"])

            emails.append(email)
            people.append([" ".join(email["name"]),"".join(email["date_time"])])

    register = {}
    for person in people:
        if not person[1] in register:
            register[person[1]] = []

        register[person[1]].append(person[0])

    return register


## Returns a list of dictionaries where each dictionary corresponds to an
## email and containing the content of the email and the sender
def get_emails():
    my_email = "bearsregister@gmail.com"
    my_password = "password goes here" #fill this in with the email password
    #ENSURE THE ABOVE PASSWORD IS NOT A PASSWORD YOU USE F0R ANYTHING ELSE.
    #THIS FILE IS NOT SECURE. THE PASSWORD IS NOT STORED AS ANYTHING BUT PLAINTEXT
    #MAKE SURE SOMEONE HAVING ACCESS TO YOUR EMAIL LISTED IS IN NO WAY
    #DAMAGING TO YOU AND THAT YOU HAVE NO SENSITIVE CONTENT ON IT

    server = imaplib.IMAP4_SSL("imap.gmail.com")
    server.login(my_email,my_password)

    server.select("inbox")
    search_data = server.search(None, "ALL")[1]

    emails = []

    for num in search_data[0].split():
        new_dict = {}
        email_data = server.fetch(num,"(RFC822)")[1][0][1]
        email_message = email.message_from_bytes(email_data)

        new_dict["from"] = email_message["from"]

        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_payload(decode=True).decode()
                new_dict["body"] = body

        emails.append(new_dict)

    return emails

## Check if the email came from warwick sport
## Done by reading and seeing if it looks right because if someone will go that
## far to fake the booking they might has well have booked it
def is_email_valid(text):
    key_lines = ["From: warwicksport@leisurecloud.net",
                 "Subject: Booking Confirmation"]

    email_lines = text.split("\n")

    flags = 0
    for line in email_lines:
        for key in key_lines:
            if key in line:
                flags += 1

    return flags == len(key_lines)

def get_original_email(text):
    ## returns the forwarded email by returning the content between the sender
    ## and the line "look forward to seeing you", this section contains the
    ## name of the person booked alongside the name and date of the session
    return text[text.index("From: warwicksport@leisurecloud.net <warwicksport@leisurecloud.net>")
                        :text.index("Total")]


## -- ALL OF THE FOLLOWING FUNCTIONS THE TEXT IS JUST THE ORIGINAL EMAIL

## Get the date and time of the session
def get_date_time(text):
    ## Gets the line of text with the date and time
    line = text.split("\n")[10]
    ## Splits the line so we can get the date and time imediatly after the ","
    ## and the returns the date and time in [day,month,year,time]
    return line.split(",")[1].split()[:4]

## Get the name of the person who booked
def get_name(email_from):
    ## Splices the line on the < and > and thenn splits on the dot to give a
    ## firstname and last name
    return email_from[email_from.index("<")+1:email_from.index("@")].split(".")
