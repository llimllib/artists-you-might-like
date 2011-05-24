import urllib

#base_url = "http://ws.audioscrobbler.com/2.0/"
#
#base_url = "http://ws.audioscrobbler.com/2.0/?"
#
#params = {"method": "artist.getsimilar", "artist": "Local Natives", 'api_key':"f3826b9e6fb686fbca1f1277f9e74861"}
#
##this is the api way. might not be necessary?
##f = urllib.urlopen(base_url + urllib.urlencode(params))
##txt = f.read()
#
#bands = ["Local Natives", "Menomena", "Tame Impala"]

def getsimilar(bands):
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
