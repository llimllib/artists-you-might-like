from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.utils import simplejson
from django.http import HttpResponse

from thepage.tasks import get_similar_bands

def index(request):
    #I would use a generic view, but I don't want to deal with the 1.2/1.3 difference. So there.
    return render_to_response("index.html", context_instance=RequestContext(request))

def similarity(request):
    bands = request.GET.getlist("b")
    #similar = getsimilar(bands)
    task_id = get_similar_bands.delay(bands).task_id
    return HttpResponse(simplejson.dumps(task_id), mimetype='application/json')

def check_result(request):
    task_id = request.GET["task_id"]
    task = get_similar_bands.AsyncResult(task_id)
    if task.ready():
        if task.state == 'SUCCESS':
            return HttpResponse(simplejson.dumps(task.result), mimetype='application/json')
        else:
            return HttpResponse(simplejson.dumps({"fail": task.result, "cause": task.traceback}), mimetype='application/json', status=500)
    else:
        return HttpResponse(simplejson.dumps("processing"), mimetype='application/json', status=202)
