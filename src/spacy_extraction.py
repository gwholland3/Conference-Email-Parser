import re
import spacy
nlp = spacy.load("en_core_web_sm")

#print(['ENT(%s)' % ent for ent in doc.ents])

def collapse_entities(doc):
    index = 0
    entities = []

    while index < len(doc.ents) - 1:
        ent1 = doc.ents[index]
        ent2 = doc.ents[index + 1]
        collapse = None
        if ent1.end + 1 == ent2.start and doc[ent1.end].text == ',':
            if ent1.label_ == 'GPE' and ent2.label_ == 'GPE':
                collapse = 'GPE'
        elif ent1.end == ent2.start:
            if ent1.label_ == 'ORDINAL' and ent2.label_ == 'EVENT':
                collapse = 'EVENT'
            elif ent1.label_ == 'DATE' and ent2.label_ == 'DATE':
                collapse = 'DATE'
        # add resulting entity to list
        if collapse is not None:
            nspan = doc[ent1.start:ent2.end]
            nspan.label_ = collapse
            index += 2
            entities.append(nspan)
        else:
            index += 1
            entities.append(ent1)

    if index < len(doc.ents):
        entities.append(doc.ents[-1])

    return entities

@spacy.Language.component('merge_named_entities')
def merge_named_entities(doc):
    # Update doc to use our collapsed entities
    entities = collapse_entities(doc)
    doc.set_ents(entities=entities, default="unmodified")

    with doc.retokenize() as retokenizer:
        for ent in doc.ents:
            retokenizer.merge(doc[ent.start:ent.end], attrs={"LEMMA": str(doc[ent.start:ent.end])})
    return doc

nlp.add_pipe('merge_named_entities')

def find_date_descendant(token):
    result = []
    if token.text in found_dates:
        result.append(token.text)
    for child in token.children:
        result += find_date_descendant(child)
    return result

texts = [
    'I would like to remind you that the abstract submission deadline for participation at the 16th Annual International Conference on Information Technology & Computer Science, 18-21 May 2020, Athens, Greece, is this coming Monday, 14 October 2019.',
    'Submission Deadline       : March 20, 2014',
    'The abstract submission deadline is 14 October 2019',
    '● Submission Deadline: February 05, 2020',
]

for text in texts:
    print(f'Processing {text}')
    text_no_parens = re.sub("[\(\[].*?[\)\]]", "", text)
    doc = nlp(text_no_parens)

    found_dates = set([e.text for e in doc.ents if e.label_ == 'DATE'])
    print(f'  Found dates: {found_dates}')

    found_event_names = set([e.text for e in doc.ents if e.label_ == 'EVENT'])
    print(f'  Found event names: {found_event_names}')

    print('  All named entities:')
    unused = [print(f'    {e.label_}: {repr(e)}') for e in doc.ents]

    deadlines = [t for t in doc if t.text.lower() == 'deadline']
    for deadline in deadlines:
        deadline_dates = []
        for right in deadline.head.rights:
            deadline_dates += find_date_descendant(right)

        immediate_lefts = [t.text.lower() for t in deadline.lefts]

        if 'submission' in immediate_lefts:
            print(f'  Submission date: {deadline_dates}')

    print(f' All tokens: {[t for t in doc]}')

#spacy.displacy.serve(doc, style="dep")

#import networkx
#import networkx as nx
#edges = []
#for token in doc:
#    for child in token.children:
#        edges.append(('{0}'.format(token.lower_),
#                      '{0}'.format(child.lower_)))
#
#graph = nx.Graph(edges)

# nx.shortest_path(graph, source='deadline', target='is')
#print(edges)
#print([[list(t.children) for t in token.children] for token in doc if token.text == 'deadline'])                             