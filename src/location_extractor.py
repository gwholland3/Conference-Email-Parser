import re

with open('country_names.txt') as f:
    country_names = [s.strip() for s in f.readlines()]
    country_abbrs = [''.join([c for c in s if c.isupper()]) for s in country_names if '&' not in s and ' ' in s]
    any_country = '|'.join(['(?:%s)' % re.escape(s) for s in country_names])
    any_abbr_country = '|'.join(['(?:%s)' % re.escape(s) for s in country_abbrs])
    country_pattern = re.compile(f'(?:.*)(?:\\s+|^)([A-Z][a-zA-Z]+),\\s*({any_country})(?:.*)', re.IGNORECASE)
    country_abbr_pattern = re.compile(f'(?:.*)(?:\\s+|^)([A-Z][a-zA-Z]+),\\s*({any_abbr_country})(?:.*)')

city_state_pattern = re.compile(f'(\s*[A-Z][a-zA-Z]+)+,\s?([A-Z][a-z]+|[A-Z][A-Z]+)')
#This mismatches dates (e.g. Friday, October) as well, may need to use with date_extractor to filter them out
def find_location(parsed_file):
    for p in parsed_file:
        for s in p:
            city_state = city_state_pattern.search(s)
            contry_full = country_pattern.match(s)
            contry_abbr = country_abbr_pattern.match(s)
            if city_state:
                return city_state.group()
            elif contry_full:
                return contry_full.group()
            elif contry_abbr:
                return contry_abbr.group()
    return "N/A"
