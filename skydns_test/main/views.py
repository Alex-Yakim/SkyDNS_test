from time import strftime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import logging

# Create your views here.
logger = logging.getLogger(__name__)


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        logger_message = {
            'time': strftime('%d/%b/%Y %H:%M:%S'),
            'url': request.path,
            'method': request.method,
            'status': HttpResponse.status_code,
            'params': email,
        }
        logger.info(logger_message)
    return render(request, 'index.html')


@csrf_exempt
def api(request):
    secret_key: str = 'ping'
    if request.method == 'GET':
        logger_message = {
            'time': strftime('%d/%b/%Y %H:%M:%S'),
            'url': request.path,
            'method': request.method,
            'status': HttpResponseNotFound.status_code,
            'params': request.GET.get('method'),
        }
        logger.info(logger_message)
        return HttpResponseNotFound('Method GET')
    elif request.method == 'POST' and request.POST.get('method') == secret_key:
        logger_message = {
            'time': strftime('%d/%b/%Y %H:%M:%S'),
            'url': request.path,
            'method': request.method,
            'status': HttpResponse.status_code,
            'params': request.GET.get('method'),
        }
        logger.info(logger_message)
        return HttpResponse('API')
    else:
        logger_message = {
            'time': strftime('%d/%b/%Y %H:%M:%S'),
            'url': request.path,
            'method': request.method,
            'status': HttpResponseBadRequest.status_code,
            'params': request.GET.get('method'),
        }
        logger.info(logger_message)
        return HttpResponseBadRequest('Method POST')
