import re
import urllib
import htmlentitydefs
import redis
import json
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
    """Given a list of bands, return a list of other bands sorted in terms of similarity

    There's two layers of caching, one for the whole query and another for each
    band. We use json to serialize data into and out of the redis store.
    """

    #TODO: expire cache keys!

    redis_conn = redis.Redis()

    logger = get_similar_bands.get_logger()
    logger.info("Getting bands: %s" % bands)

    #let's see if the whole query is in the cache
    bands = sorted(bands)
    querykey = "ayml-querycache-%s" % "".join(bands)
    qcache = redis_conn.get(querykey)
    if qcache:
        logger.info("hit the query cache for %s" % querykey)
        return json.loads(qcache)

    #a dictionary of <band name>: (total score, # of appearances, bandname)
    similar = {}

    for band in bands:
        key = "ayml-bandcache-%s" % band
        bcache = redis_conn.get(key)
        if bcache:
            logger.info("hit the band cache for %s" % key)
            text = json.loads(bcache)
        else:
            url = "http://ws.audioscrobbler.com/2.0/artist/%s/similar.txt" % band
            logger.info("Fetching url: %s" % url)
            text = urllib.urlopen(url).read()
            redis_conn.set(key, json.dumps(text))

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

    final = sorted(final, reverse=True)

    redis_conn.set(querykey, json.dumps(final))

    return final
