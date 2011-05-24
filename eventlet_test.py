from eventlet import wsgi
import eventlet

import urllib
from urlparse import parse_qs

base_url = "http://ws.audioscrobbler.com/2.0/"

base_url = "http://ws.audioscrobbler.com/2.0/?"

bands = ["Local Natives", "Menomena", "Tame Impala"]

def get_similar(bands):
    #a dictionary of <band name>: (total score, # of appearances, bandname)
    similar = {}

    for band in bands:
        text = urllib.urlopen("http://ws.audioscrobbler.com/2.0/artist/%s/similar.txt" % band).read()
        for line in text.split("\n"):
            if not line: continue

            similarity, mbid, bandname = line.split(",")
            similarity = float(similarity)

            if bandname in similar:
                score, n = similar[bandname]
                similar[bandname] = (score + similarity, n+1)
            else:
                similar[bandname] = (similarity, 1)

    final = []
    for name, (score, n) in similar.iteritems():
        final.append((score * (n**2), score, n, name))

    return sorted(final, reverse=True)

def hello_world(env, start_response):
    if env['PATH_INFO'] != '/':
        start_response('404 Not Found', [('Content-Type', 'text/plain')])
        return ['Not Found\r\n']
    
    start_response('200 OK', [('Content-Type', 'text/plain')])
    params = parse_qs(env["QUERY_STRING"])
    similar = get_similar(params['b'])
    ret = "\n".join(band for _, _, _, band in similar[:30])
    #import pdb; pdb.set_trace()
    print "success!"
    return [ret]

wsgi.server(eventlet.listen(('', 8090)), hello_world)
