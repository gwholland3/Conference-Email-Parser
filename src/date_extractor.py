import nltk
import re
#import spacy
from dateutil import parser

def standardize_date(date_string):
    parsed_date = parser.parse(date_string,fuzzy=True)
    return parsed_date.date().isoformat()

def find_dates(parsed_file):
    '''
    :param This function takes as input a parsed eml file.
    :return: dict of values to dates
    '''
    date_dict = {'conf_dates': None, 'submission_deadline': [], 'notif_deadline': None}
    #for p in parsed_file:
    for s in parsed_file:
        for w in s:
            #find if word has a number from 2000 to 2040 because that is likely a date
            match = re.search(r"\b(20[0-3]\d|2040)\b", w)
            if match:
                #check to see what type of date it is
                pattern = r"\d|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec"
                filtered_strings = [i for i in s if re.search(pattern,i,flags=re.IGNORECASE)][:3]
                date_string = ' '.join(filtered_strings)
                try:
                    standardized = standardize_date(date_string)
                except:
                    continue
                if is_conference_date(s,w):
                    #print(s)
                    current_sentence = ' '.join(filtered_strings)
                    if date_dict['conf_dates'] == None:
                        date_dict['conf_dates'] = current_sentence
                    elif len(current_sentence) < len(date_dict['conf_dates']):
                        date_dict['conf_dates'] = current_sentence
                if is_submission_date(s,w):
                    date_dict['submission_deadline'].append(standardized)
                if is_notification_date(s,w):
                    date_dict['notif_deadline'] = standardized

    if len(date_dict['submission_deadline']) > 0:
        date_dict['submission_deadline'] = date_dict['submission_deadline'][0]
    else:
        date_dict['submission_deadline'] = None
    return date_dict


def is_submission_date(parsed_sentence,date_word):
    '''
    :param parsed_sentence: a parsed sentence that contains a date
    :param date_word: word that was found to contain a date
    :return: true or false on whether or not sentence is considered a submission deadline
    '''
    #features to be found
    is_proper_date = False
    contains_month = False
    contains_submission = False
    #check if the date is a proper date
    match = re.search(r'\d{4}-\d{2}-\d{2}', date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{2}-\d{2}-\d{4}', date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', date_word)
    if match:
        is_proper_date = True
    months = ['jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    #check if there are other factors that suggest this is a submission date
    for w in parsed_sentence:
        if 'submission' in w.lower():
            contains_submission = True
        for month in months:
            if month in w.lower():
                contains_month = True
    if contains_submission and (contains_month or is_proper_date):
        return True
    return False

def is_notification_date(parsed_sentence,date_word):
    '''
    :param parsed_sentence: a parsed sentence that contains a date
    :param date_word: word that was found to contain a date
    :return: true or false on whether or not sentence is considered a submission deadline
    '''
    #features to be found
    is_proper_date = False
    contains_month = False
    contains_notification = False
    #check if the date is a proper date
    match = re.search(r'\d{4}-\d{2}-\d{2}', date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{2}-\d{2}-\d{4}', date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{1,2}/\d{1,2}/\d{4}', date_word)
    if match:
        is_proper_date = True
    months = ['jan', 'feb', 'mar', 'apr', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
    #check if there are other factors that suggest this is a submission date
    for w in parsed_sentence:
        if 'notification' in w.lower():
            contains_notification = True
        for month in months:
            if month in w.lower():
                contains_month = True
    if contains_notification and (contains_month or is_proper_date):
        return True
    return False

def is_conference_date(parsed_sentence,date_word):
    '''
    :param parsed_sentence: a parsed sentence that contains a date
    :param date_word: word that was found to contain a date
    :return: true or false on whether or not sentence is considered a conference date
    '''
    #features to be found
    is_proper_date = False
    contains_month = False
    contains_conferenece = False
    #check if date is a proper date
    match = re.search(r'\d{4}-\d{2}-\d{2}',date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{2}-\d{2}-\d{4}',date_word)
    if match:
        is_proper_date = True
    match = re.search(r'\d{1,2}/\d{1,2}/\d{4}',date_word)
    if match:
        is_proper_date = True
    months = ['jan','feb','mar','apr','jun','jul','aug','sep','oct','nov','dec']
    #check if there are other factors that suggest this is a conference date
    for w in parsed_sentence:
        if 'conference' in w.lower():
            contains_conferenece = True
        for month in months:
            if month in w.lower():
                contains_month = True
    if contains_conferenece and (contains_month or is_proper_date):
        return True
    return False

#This stuff just used for testing
# if __name__ == '__main__':
#     f = open('../out/id349.html.txt','r')
#     text = f.read()
#     sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#     parsed = [[nltk.word_tokenize(s) for s in sent_tokenizer.tokenize(par.strip())] for par in text.split('\n')]
#     print(parsed)
#     print(find_dates(parsed))
#     nlp = spacy.load("en_core_web_sm")
#     doc = nlp(text)
#     for entity in doc.ents:
#         if entity.label_ == "DATE":
#             print(entity.text)
#             for token in entity.subtree:
#                 if token.head == entity.root:
#                     print(token.text, token.head)
#     f.close()
