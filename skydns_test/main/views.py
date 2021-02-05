from time import strftime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import logging

# Создаем экземпляр логгера
logger = logging.getLogger(__name__)


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        """Сообщение для логгера"""
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
        """Если GET запрос, записываем в логи, выдаем 404 ошибку"""
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
        """Если пришел POST запрос с нужными параметрами, выдаем 200 код"""
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
        """В остальных случаях выдем 400 ошибку"""
        logger_message = {
            'time': strftime('%d/%b/%Y %H:%M:%S'),
            'url': request.path,
            'method': request.method,
            'status': HttpResponseBadRequest.status_code,
            'params': request.GET.get('method'),
        }

        logger.info(logger_message)
        return HttpResponseBadRequest('Method POST')
