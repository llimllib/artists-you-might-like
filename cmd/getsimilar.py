import urllib

def getsimilar(bands):
    #a dictionary of <band name>: (total score, # of appearances, bandname)
    similar = {}

    for band in bands:
        url = "http://ws.audioscrobbler.com/2.0/artist/%s/similar.txt" % urllib.quote(band)
        text = urllib.urlopen(url).read()
        print "opening %s" % url
        for line in text.split("\n"):
            if not line: continue

            try:
                similarity, mbid, bandname = line.split(",", 2)
            except ValueError:
                print "failed to parse: %s" % line
                continue
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

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Given a list of bands, return similar bands they have in common')
    parser.add_argument('bands', metavar='bands', help='A comma-separated list of band names')
    args = parser.parse_args()
    
    bands = args.bands.split(",")
    print "searching %s" % bands

    similar = getsimilar(bands)
    for score, score2, n, name in similar:
        if n > 1:
            print "%s (%d)" % (name, n)
