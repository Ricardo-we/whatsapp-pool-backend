from uuid import uuid1
from django.http import HttpResponse, JsonResponse
from ..models import User, Categorie, Messages
from ..serializers import MessagesSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from ..views import SUCCESS_MESSAGE, ERROR_MESSAGE
from utils.models_utils import ModelUtils
from utils.scheduler import validate_cron_exp, scheduler, cron_scheduler, delete_job_if_exists
from services.message_types.MessageContext import execute_method


def mail_template(message):
    def execute_():
        execute_method(message, type=message.message_type)
    return execute_


def get_scheduled_message_id(message_id):
    return "msg-id-" + str(message_id)


@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def create_message(request):
    try:
        user = User.check_user_token(request.data['user_id'], request=request, returning=True)
        validate_cron_exp(request.data.get("message_interval"))

        message = ModelUtils.insert_into_model(Messages, request.data)

        if request.data.get("message_interval"):
            schedule_id = get_scheduled_message_id(message.id)
            cron_scheduler(mail_template(message), schedule_id, request.data["message_interval"])

        serializer = MessagesSerializer(message, many=False)
        return Response(serializer.data)
    except Exception as error:
        print(error)
        return JsonResponse(ERROR_MESSAGE(error))


def get_message(message):
    try:
        serializer = MessagesSerializer(message, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False)


def update_message(request, message):
    schedule_id = get_scheduled_message_id(message.id)
    delete_job_if_exists(schedule_id)

    ModelUtils.update_model_obj(message, request.data, invalid_fields=["user_id"])

    if request.data.get("message_interval"):
        validate_cron_exp(request.data.get("message_interval"))
        cron_scheduler(mail_template(message), schedule_id, request.data["message_interval"])

    serializer = MessagesSerializer(message, many=False)
    return Response(serializer.data)


@csrf_exempt
@api_view(['PUT', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def message_details(request, message_id):
    try:
        if not User.check_user_token(request.data.get('user_id'), request=request):
            raise Exception('Invalid token or user_id')

        message = Messages.objects.get(id=message_id)

        if request.method == 'DELETE':
            schedule_id = get_scheduled_message_id(message.id)
            if(message.message_interval and scheduler.get_job(schedule_id)):
                scheduler.remove_job(schedule_id)
            message.delete()
            return JsonResponse(SUCCESS_MESSAGE, safe=False)
        elif request.method == 'GET':
            return get_message(message)
        elif request.method == 'PUT':
            return update_message(request, message)

    except Exception as error:
        print(error)
        return JsonResponse(ERROR_MESSAGE(error), safe=False, status=409)
