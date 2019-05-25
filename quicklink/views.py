import logging

from django.http.response import JsonResponse
from django.shortcuts import render, redirect

from . import env


logger = logging.getLogger(__name__)

def root(request):
    if request.method == 'GET':
        return redirect('/QuickLink/')

def homepage(request):
    return redirect('/QuickLink/home/')

def envinfo(request):
    jsondata = {}
    currenv = env.get_env()
    currloglevel = env.get_log_level();
    currdb = env.get_database().get('NAME', None)
    jsondata['env'] = currenv
    jsondata['loglevel'] = currloglevel
    jsondata['database'] = currdb
    return JsonResponse(jsondata) 
    
    
def bad_request(request, exception):
    context = {}
    context['errorcode'] = '400 Bad Request'
    context['errormsg'] = 'Invalid Request!'
    return render(request, 'common/error.html', context)
    return render(request, '')

def permission_denied(request, excpetion):
    context = {}
    context['errorcode'] = '403 Permission Denied'
    context['errormsg'] = 'Not authorized to view content!'
    return render(request, 'common/error.html', context)
    return render(request, '')

def page_not_found(request, exception):
    context = {}
    context['errorcode'] = '404 Page Not Found'
    context['errormsg'] = 'Requested page not found!'
    return render(request, 'common/error.html', context)

def server_error(request):
    context = {}
    context['errorcode'] = '500 Server Internal Error'
    context['errormsg'] = 'Something wrong with server!'
    return render(request, 'common/error.html', context)
    return render(request, '')
