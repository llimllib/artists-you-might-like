from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

def index(request):
    #I would use a generic view, but I don't want to deal with the 1.2/1.3 difference. So there.
    return render_to_response("index.html", context_instance=RequestContext(request))
