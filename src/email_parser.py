import email
import os
import email.header
import codecs
from bs4 import BeautifulSoup

path = 'data/conf_emails_numbered/'
listing = os.listdir(path)

# Parsing limit for testing.
limit = 10

def get_header(msg, name):
    text, encoding = email.header.decode_header(msg.get(name))[0]
    if isinstance(text, bytes):
        text = text.decode(encoding=encoding)
    return text.replace('\n', ' ').replace('  ', ' ')

for filename in listing:
    msg = email.message_from_file(open(path + filename))

    details = {
        'subject': get_header(msg, 'subject'),
        'from': get_header(msg, 'from'),
        'to': get_header(msg, 'to'),
        'date': get_header(msg, 'date'),
    }

    for part in msg.walk():
        if part.get_content_type() == 'text/html':
            html = part.get_payload(decode=True).decode(part.get_content_charset())
            soup = BeautifulSoup(html, features="html.parser")
            with open('out/' + filename.replace('eml', 'html'), 'wb') as f:
                f.write(soup.prettify().encode('utf-8'))

            for tag in soup(["title"]):
                details['title'] = tag.extract().get_text()

            # I've found that this is a pretty good way to tokenize HTML emails.
            # It's easier to begin with a split-up representation and re-join if
            # needed.
            extracted = [s.strip() for s in soup.strings if not s.isspace()]

            with open('out/%s.txt' % filename.replace('eml', 'html'), 'wb') as f:
                f.write('\n'.join(extracted).encode('utf-8'))

    print(details)

    limit -= 1
    if limit < 0:
        break
