import email
import os
import email.header
import codecs
import re
from bs4 import BeautifulSoup
#from nltk.corpus import brown as br


class Email:

    def __init__(self, subject, body_text):
        self.subject = subject
        self.body_text = body_text


# Country names list taken from:
# https://gist.githubusercontent.com/kalinchernev/486393efcca01623b18d/raw/daa24c9fea66afb7d68f8d69f0c4b8eeb9406e83/countries
with open('country_names.txt') as f:
    country_names = [s.strip() for s in f.readlines()]
    country_abbrs = [''.join([c for c in s if c.isupper()]) for s in country_names if '&' not in s and ' ' in s]
    #print(country_abbrs)
    any_country = '|'.join(['(?:%s)' % re.escape(s) for s in country_names])
    any_abbr_country = '|'.join(['(?:%s)' % re.escape(s) for s in country_abbrs])
    #print(any_country)
    country_pattern = re.compile(f'(?:.*)(?:\\s+|^)([A-Z][a-zA-Z]+),\\s*({any_country})(?:.*)', re.IGNORECASE)

    # Do not ignore case here
    country_abbr_pattern = re.compile(f'(?:.*)(?:\\s+|^)([A-Z][a-zA-Z]+),\\s*({any_abbr_country})(?:.*)')


#with open('country_names.txt') as f:
#    country_names = [s.strip() for s in f.readlines()]
#    any_country = '|'.join(['(?:%s)' % re.escape(s) for s in ['Japan']])
#    country_pattern = re.compile(f'(?:.*)({any_country})(?:.*)', re.IGNORECASE)
#    print(country_pattern.match('Japan'))


def process_email(email_file):
    with open(email_file) as f:
        msg = email.message_from_file(f)

    subject = get_header(msg, 'subject')

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

                """
                for x in extracted:
                    match = country_pattern.match(x)
                    if match:
                        print('  ' + str(match.groups()))
                    match = country_abbr_pattern.match(x)
                    if match:
                        print('  ' + str(match.groups()))
                """

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
