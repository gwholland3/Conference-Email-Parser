from bs4 import BeautifulSoup


# This file is the HTML template for our dashboard page
TEMPLATE_FILEPATH = 'docs/index_template.html'

# This file holds the current contents of our dashboard page
DASHBOARD_FILEPATH = 'docs/index.html'

# Which fields/columns we support to display in the dashboard table
# Key is the name used internally, value is the display name on the dashboard
supported_fields = {
        'source_name': "Source Name",
        'conf_name': "Conference Name",
        'description': "Description",
        'location': "Location",
        'conf_start_date': "Start Date",
        'conf_end_date': "End Date",
        'submission_deadline': "Submission Deadline",
        'notif_deadline': "Notification Deadline"
}


def add_to_dashboard(email_summaries, append=False):
    """
    Add email summaries to the dashboard.

    email_summaries is a list of dicts containing email information.

    append=False overwrites the existing contents in index.html,
    append=True appends the new parsed emails following the existing ones.
    """

    soup, table = get_table(append)

    if table.thead.tr is None:
        header_row = soup.new_tag('tr')
        table.thead.append(header_row)
        for field in supported_fields:
            th = soup.new_tag('th')
            header_row.append(th)
            th.append(supported_fields[field])
        
    for parsed_email in email_summaries:
        email_row = soup.new_tag('tr')
        table.tbody.append(email_row)
        for field in supported_fields:
            td = soup.new_tag('td')
            email_row.append(td)
            content = parsed_email[field] if field in parsed_email and parsed_email[field] is not None  else "N/A"
            td.append(content)

    with open(DASHBOARD_FILEPATH, 'w') as f:
        f.write(soup.prettify())


def get_table(append):
    if append:
        try:
            with open(DASHBOARD_FILEPATH) as f:
                soup = BeautifulSoup(f, 'html.parser')
            table = soup.find('table')
            if table:
                return soup, table
            print("Existing index.html doesn't have table element, generating new file")
        except:
            print("Couldn't find existing index.html, generating new file")

    with open(TEMPLATE_FILEPATH) as f:
        soup = BeautifulSoup(f, 'html.parser')
    table = soup.find('table')
    
    return soup, table


# Test script
if __name__ == '__main__':
    email_summaries = [{'source_name': 'email1', 'conf_name': 'conf1'}, {'source_name': 'email2'}]
    add_to_dashboard(email_summaries, append=True)
