import imaplib
import email

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

## Goes through the inbox and deletes any bookings for sessions that have
## already happened
def clean_inbox():
    pass
