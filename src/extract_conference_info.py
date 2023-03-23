import os

import nltk

from email_parser import process_email
from location_extractor import find_location
from conference_extractor import find_conference
from date_extractor import find_dates
from dashboard import add_to_dashboard


# Where the emails to be parsed are located
emails_dir = 'data/conf_emails_numbered'
# How many emails to parse from above location
num_emails = 30

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

def main():
    email_summaries = []

    # Get the filenames of all the email files to be parsed
    email_files = [f'{emails_dir}/{filename}' for filename in os.listdir(emails_dir)][:num_emails]

    for email_file in email_files:
        # Process the raw email file to extract the relevant data we will need for parsing
        processed_email = process_email(email_file)
        if processed_email is None:
            continue

        email_info = {'source_name': email_file}

        sent_tokenized_content = [[s for s in sent_tokenizer.tokenize(par.strip())] for par in processed_email.body_text.split('\n')]
        word_tokenized_content = [nltk.word_tokenize(s) for p in sent_tokenized_content for s in p]

        email_info['location'] = find_location(sent_tokenized_content)

        email_info['conf_name'] = find_conference(sent_tokenized_content)

        conf_dates = find_dates(word_tokenized_content)
        email_info.update(conf_dates)

        email_summaries.append(email_info)

    # Insert our conference email summaries into our HTML dashboard
    add_to_dashboard(email_summaries)


if __name__ == '__main__':
    main()
