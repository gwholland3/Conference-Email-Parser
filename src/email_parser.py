import email
import email.header
import os

from bs4 import BeautifulSoup


# Email object acts as a uniform container of relevant email data for our extractors to take in
class Email:

    def __init__(self, subject, body_text):
        # The subject line of the email
        self.subject = subject

        # All of the text in the message body, concatenated
        self.body_text = body_text


def process_email(email_file):
    """
    Reads the raw contents of the .eml file, and pulls out all the data
    we want into an Email object that gets returned.

    Returns `None` if there is nothing to extract from the email.
    """

    with open(email_file) as f:
        msg = email.message_from_file(f)

    subject = msg.get('subject')

    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_payload(decode=True).decode(part.get_content_charset())
            soup = BeautifulSoup(html, 'html.parser')

            # I've found that this is a pretty good way to tokenize HTML emails.
            # It's easier to begin with a split-up representation and re-join if
            # needed.
            strings = [s.strip() for s in soup.strings if not s.isspace()]
            body_text = '\n'.join(strings)

            return Email(subject, body_text)

    return None


def parse_emails(emails_dir, out_dir, limit=None):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    listing = os.listdir(emails_dir)
    count = 0

    for filename in listing:
        msg = email.message_from_file(open(f'{emails_dir}/{filename}'))

        details = {
            'subject': get_header(msg, 'subject'),
            'from': get_header(msg, 'from'),
            'to': get_header(msg, 'to'),
            'date': get_header(msg, 'date'),
        }

        #print('%s: %s\n' % (filename, details['subject']))

        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html = part.get_payload(decode=True).decode(part.get_content_charset())
                soup = BeautifulSoup(html, features="html.parser")
                with open(f'{out_dir}/' + filename.replace('eml', 'html'), 'wb') as f:
                    f.write(soup.prettify().encode('utf-8'))

                for tag in soup(["title"]):
                    details['title'] = tag.extract().get_text()

                # I've found that this is a pretty good way to tokenize HTML emails.
                # It's easier to begin with a split-up representation and re-join if
                # needed.
                extracted = [s.strip() for s in soup.strings if not s.isspace()]

                with open(f'{out_dir}/%s.txt' % filename.replace('eml', 'html'), 'wb') as f:
                    f.write('\n'.join(extracted).encode('utf-8'))

        #print(details)

        count += 1
        if limit and count >= limit:
            break


def get_header(msg, name):
    text, encoding = email.header.decode_header(msg.get(name))[0]
    if isinstance(text, bytes):
        text = text.decode(encoding=encoding) if encoding else str(text)
    return text.replace('\n', ' ').replace('  ', ' ')
