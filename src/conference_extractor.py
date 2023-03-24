import re
#May miss some names if only abbreviation is available
titlecase = '(\s*[A-Z][a-zA-Z]+)+'
conf_pattern = re.compile(f'{titlecase}\s*[Cc]onference( on{titlecase})(.*[0-9]{4})?')
conf_pattern_2 = re.compile(f'([0-9]{4})?{titlecase}\s*[Cc]onference')
conf_pattern_fallback = re.compile(f'{titlecase} on{titlecase}')

def find_conference(parsed_file):
    for p in parsed_file:
        for s in p:
            if 'onference' in s:
                conference = conf_pattern.search(s)
                if conference:
                    return conference.group()

                conference = conf_pattern_2.search(s)
                if conference:
                    return conference.group()
            
            if 'on' in s:
                conference = conf_pattern_fallback.search(s)
                if conference:
                    return conference.group()
    return "N/A"

