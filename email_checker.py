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
