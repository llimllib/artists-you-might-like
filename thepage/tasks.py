import re
import urllib
import htmlentitydefs
from celery.task import task

def replace_entities(match):
    """ ask maze. """ 
    ent = match.group() 
    return htmlentitydefs.entitydefs.get(ent[1:-1]) 

def html_unescape(data): 
    ''' unescape (numeric) HTML entities. '''
    return re.sub(r"&[A-Za-z0-9]+?;", replace_entities, data) 

@task
def get_similar_bands(bands):
    logger = get_similar_bands.get_logger()
    logger.info("Getting bands: %s" % bands)

    #a dictionary of <band name>: (total score, # of appearances, bandname)
    similar = {}

    for band in bands:
        text = urllib.urlopen("http://ws.audioscrobbler.com/2.0/artist/%s/similar.txt" % band).read()
        for line in text.split("\n"):
            if not line: continue

            similarity, mbid, bandname = html_unescape(line).split(",", 2)
            similarity = float(similarity)

            if bandname in similar:
                score, n = similar[bandname]
                similar[bandname] = (score + similarity, n+1)
            else:
                similar[bandname] = (similarity, 1)

    final = []
    for name, (score, n) in similar.iteritems():
        final.append((score * (n**2), score, n, name))

    #TODO: store this shit in redis? How to return the value?
    return sorted(final, reverse=True)
