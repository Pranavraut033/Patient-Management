from django.http import HttpResponseRedirect, HttpResponse, Http404

def a(request):
    print(request.POST)
    raise Http404
