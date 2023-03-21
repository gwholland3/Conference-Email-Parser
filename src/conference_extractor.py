import re
#May miss some names if only abbreviation is available
conf_pattern = re.compile(f'(\s*[A-Z][a-zA-Z]+)+\s*[Cc]onference(.*[0-9]{4})?')

def find_conference(parsed_file):
    for p in parsed_file:
        for s in p:
            conference = conf_pattern.search(s)
            if conference:
                return conference.group()
    return "N/A"

