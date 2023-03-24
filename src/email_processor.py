import email
import email.policy
import html2text
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

    Returns `None` if it can't process the email file.
    """

    try:
        with open(email_filename, encoding="ISO-8859-1") as f:
            msg = email.message_from_file(f, policy=email.policy.default)
    except:
        print(f"Error processing email file {email_filename}")
        return None

    subject = get_header_field(msg, 'Subject')
    sender = get_header_field(msg, 'From')

    # Would be nice, but there are random edge cases that make this annoying to parse
    #sender_name, sender_addr = parse_sender(sender)

    # Prefer plaintext version, but HTML can be converted
    body = msg.get_body(('plain', 'html'))
    body_text = body.get_content().strip()

    # Convert HTML to plaintext if necessary
    if body.get_content_subtype() == 'html':
        body_text = html2text.html2text(body_text)

    return Email(sender, subject, body_text)


def get_header_field(msg, name):
    # Retrieves the value of a named header field and cleans it up
    return re.sub(r'\s+', ' ', decode_header(msg.get_all(name)[0]).strip())


def decode_header(header_val):
    # Handles the decoding and reconstruction of the complete string
    return str(email.header.make_header(email.header.decode_header(header_val)))


def parse_sender(sender):
    # Split the full sender string into the sender display name and their email address
    return re.match(r'^"?(.*?)"? ?<([\w\.-]+@[\w\.-]+)>$', sender).groups()
