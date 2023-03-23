import os

import nltk

from email_parser import process_email
from location_extractor import find_location
from conference_extractor import find_conference
from date_extractor import find_dates
from dashboard import add_to_dashboard


# Where the emails to be parsed are located
emails_dir = 'data/conf_emails_numbered'
# Maximum number of emails to parse from above location (set to `None` for no limit)
limit = 20

sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')


def main():
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
        email_info = {'source_name': filename}

        sent_tokenized_content = [[s for s in sent_tokenizer.tokenize(par.strip())] for par in processed_email.body_text.split('\n')]
        word_tokenized_content = [nltk.word_tokenize(s) for p in sent_tokenized_content for s in p]

        email_info['location'] = find_location(sent_tokenized_content)

        email_info['conf_name'] = find_conference(sent_tokenized_content)

        conf_dates = find_dates(word_tokenized_content)
        email_info.update(conf_dates)

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


if __name__ == '__main__':
    main()
