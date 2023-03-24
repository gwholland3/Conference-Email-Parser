import email
import email.policy
import html2text
import os
import re


# Email object acts as a uniform container of relevant email data for our extractors to take in
class Email:

    def __init__(self, sender, subject, body_text):
        # "From" header field
        self.sender = sender

        # The subject line of the email
        self.subject = subject

        # All of the text in the message body, concatenated
        self.body_text = body_text


def process_email(email_filename):
    """
    Reads the raw contents of the .eml file, and pulls out all the data
    we want into an Email object that gets returned.
    """

    with open(email_filename) as f:
        msg = email.message_from_file(f, policy=email.policy.default)

    subject = get_header_field(msg, 'Subject')
    sender = get_header_field(msg, 'From')

    #sender_name, sender_addr = parse_sender(sender)

    body = msg.get_body(('plain', 'html'))
    body_text = body.get_content().strip()
    if body.get_content_subtype() == 'html':
        body_text = html2text.html2text(body_text)

    return Email(sender, subject, body_text)


def get_header_field(msg, name):
    return re.sub(r'\s+', ' ', decode_header(msg.get_all(name)[0]).strip())


def decode_header(header_val):
    return str(email.header.make_header(email.header.decode_header(header_val)))


def parse_sender(sender):
    return re.match(r'^"?(.*?)"? ?<([\w\.-]+@[\w\.-]+)>$', sender).groups()
