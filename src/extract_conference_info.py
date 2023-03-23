import os

import nltk

from email_parser import parse_emails
from location_extractor import find_location
from date_extractor import find_dates
from dashboard import add_to_dashboard


emails_dir = 'data/conf_emails_numbered'
out_dir = 'processed_emails'

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def main():
    parse_emails(emails_dir, out_dir, limit=10)

    emails = []

    listing = [filename for filename in os.listdir(out_dir) if filename.endswith('.txt')]
    for filename in listing:
        email_info = {}
        with open(f'{out_dir}/{filename}') as f:
            content = f.read()
        sent_tokenized_content = [[s for s in sent_tokenizer.tokenize(par.strip())] for par in content.split('\n')]
        word_tokenized_content = [nltk.word_tokenize(s) for p in sent_tokenized_content for s in p]

        email_info['location'] = find_location(sent_tokenized_content)

        conf_dates = find_dates(word_tokenized_content)
        email_info.update(conf_dates)

        emails.append(email_info)

    add_to_dashboard(emails)


if __name__ == '__main__':
    main()
