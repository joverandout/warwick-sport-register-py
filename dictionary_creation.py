#!/usr/bin/env python

## The file that is run
import email_functions
import email_checker
import json


def dictionary_creation():
    emails = []
    people = []

    for email in email_functions.get_emails():
        if email_checker.is_email_valid(email["body"]):
            email["body"] = email_checker.get_original_email(email["body"])
            email["date_time"] = email_checker.get_date_time(email["body"])
            email["name"] = email_checker.get_name(email["from"])

            emails.append(email)
            people.append([" ".join(email["name"]),"".join(email["date_time"])])

    register = {}
    for person in people:
        if not person[1] in register:
            register[person[1]] = []

        register[person[1]].append(person[0])

    return register