from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from artists_you_might_like.utils.getsimilar import getsimilar

def index(request):
    #I would use a generic view, but I don't want to deal with the 1.2/1.3 difference. So there.
    return render_to_response("index.html", context_instance=RequestContext(request))

def similarity(request):
    bands = request.GET.getlist("b")
    similar = getsimilar(bands)
    return HttpResponse(simplejson.dumps(similar), mimetype='application/json')
