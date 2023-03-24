import argparse
import os
import sys

import nltk

from email_processor import process_email
from location_extractor import find_location
from conference_extractor import find_conference
from date_extractor import find_dates
from spacy_extraction import spacy_parse_email
from dashboard import add_to_dashboard


# Default value for emails_dir
DEFAULT_EMAILS_DIR = 'data/conf_emails_numbered'

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def main(emails_dir, limit):
    """
    Main driver of the script, orchestrates the various phases of extracting
    info from the conference emails in the direcotry specified by `emails_dir`.
    """

    # Get the filenames of all the email files
    email_filenames = [f'{emails_dir}/{filename}' for filename in os.listdir(emails_dir)]

    # Process each email (up to our limit) and convert it into a uniform Email object for parsing
    processed_emails = process_emails(email_filenames)

    email_summaries = []
    # Generate an information summary for each email
    for filename, processed_email in processed_emails:
        print(filename)
        email_info = {'source_name': filename}

        sent_tokenized_content = [[s for s in sent_tokenizer.tokenize(par.strip())] for par in processed_email.body_text.split('\n')]
        word_tokenized_content = [nltk.word_tokenize(s) for p in sent_tokenized_content for s in p]

        #email_info['location'] = find_location(sent_tokenized_content)

        email_info['conf_name'] = None#find_conference(sent_tokenized_content)

        conf_dates = find_dates(word_tokenized_content)
        email_info.update(conf_dates)

        spacy_info = spacy_parse_email(processed_email.body_text)
        email_info.update(spacy_info)

        email_summaries.append(email_info)

    # Insert our conference email summaries into our HTML dashboard
    add_to_dashboard(email_summaries)


def process_emails(email_filenames):
    """
    Takes in a list of email filenames and returns a list
    of tuples, each tuple containing the filename and the Email
    object that has the extracted email data we want.
    """

    processed_emails = []
    count = 0
    for email_filename in email_filenames:
        if limit and count >= limit:
            break

        # Process the raw email file to extract the relevant data we will need for parsing
        processed_email = process_email(email_filename)

        if processed_email is None:
            # Something is wrong with the email, or it doesn't contain any content we wanted
            continue

        processed_emails.append((email_filename, processed_email))
        count += 1

    return processed_emails


def get_args():
    parser = argparse.ArgumentParser(description="Extract conference information from emails")
    parser.add_argument('emails_dir', nargs='?', default=DEFAULT_EMAILS_DIR, help="directory containg the emails to be analyzed")
    parser.add_argument('-l', '--limit', type=positive_int, help="maximum number of emails to analyze in the emails directory")
    args = parser.parse_args()

    return args.emails_dir, args.limit


def positive_int(val):
    int_val = int(val)
    if int_val <= 0:
        raise argparse.ArgumentTypeError(f"{value} is an invalid positive int value")
    return int_val


if __name__ == '__main__':
    emails_dir, limit = get_args()

    main(emails_dir, limit)
