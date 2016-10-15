import sys, os
# Make sure you put the mitielib folder into the python search path.  There are
# a lot of ways to do this, here we do it programmatically with the following
# two statements:
from geopy.geocoders import Nominatim
geolocator = Nominatim()

from mitie import *
from collections import defaultdict

import itertools
import operator

def most_common(L):
    if len(L) == 0:
      return None
    # get an iterable of (item, iterable) pairs
    SL = sorted((x, i) for i, x in enumerate(L))
    # print 'SL:', SL
    groups = itertools.groupby(SL, key=operator.itemgetter(0))
    # auxiliary function to get "quality" for an item
    def _auxfun(g):
        item, iterable = g
        count = 0
        min_index = len(L)
        for _, where in iterable:
          count += 1
          min_index = min(min_index, where)
        # print 'item %r, count %r, minind %r' % (item, count, min_index)
        return count, -min_index
    # pick the highest-count/earliest item
    return max(groups, key=_auxfun)[0]

ner = named_entity_extractor('MITIE-models/ner_model.dat')
print "\nTags output by this NER model:", ner.get_possible_ner_tags()

# Load a text file and convert it into a list of words.
def get_location(text2):
    tokens = tokenize(text2)
    print "Tokenized input:", tokens

    entities = ner.extract_entities(tokens)
    print "\nEntities found:", entities
    print "\nNumber of entities detected:", len(entities)

    # entities is a list of tuples, each containing an xrange that indicates which
    # tokens are part of the entity, the entity tag, and an associate score.  The
    # entities are also listed in the order they appear in the input text file.
    # Here we just print the score, tag, and text for each entity to the screen.
    # The larger the score the more confident MITIE is in its prediction.
    locations = []
    for e in entities:
        range = e[0]
        tag = e[1]
        score = e[2]
        score_text = "{:0.3f}".format(score)
        if tag =='LOCATION':
            entity_text = " ".join(tokens[i] for i in range)
            locations.append(entity_text)
        return most_common(locations)

def generate_geojson(place, title):
    geo = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [0, 0]
          },
            "properties": {
                "name": ""
            }
        }
    if place is not None:
        location = geolocator.geocode(place)
        latitude = location.latitude
        longitude = location.longitude
        geo["geometry"]["coordinates"] = [latitude, longitude]
    if title is not None:
        geo["properties"]['name'] = title
    return geo
