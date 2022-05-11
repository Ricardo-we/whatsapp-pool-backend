from django.http import HttpResponse, JsonResponse
from api.models import User, Categorie, Messages
from api.serializers import MessagesSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.views import SUCCESS_MESSAGE, ERROR_MESSAGE
from pywhatkit import whats

@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def create_message(request):
    try:
        if not User.check_user_token(request.data['user_id'], request=request): 
            raise Exception('Invalid token or user_id')
        
        message = Messages.objects.create(
            message_to=request.data['message_to'],
            categorie_id=request.data.get('categorie_id') or None,
            message_to_number=request.data.get('message_to_number'),
            message=request.data['message'], 
            user_id=request.data['user_id']
        )
        serializer = MessagesSerializer(message, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error)) 

def get_message(message):
    try:
        serializer = MessagesSerializer(message, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False)

def update_message(request,message):
    if request.data.get('message'): message.message = request.data.get('message')  
    if request.data.get('message_to'): message.message_to = request.data.get('message_to')  
    if request.data.get('categorie_id'): message.categorie_id = request.data.get('categorie_id')
    if request.data.get('message_to_number'): message.message_to_number = request.data.get('message_to_number')

    message.save()
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
            message.delete()
            return JsonResponse(SUCCESS_MESSAGE, safe=False)
        elif request.method == 'GET': 
            return get_message(message)
        elif request.method == 'PUT':
            return update_message(request, message)

    except Exception as error:
        print(error)
        return JsonResponse(ERROR_MESSAGE(error), safe=False, status=409)


# @csrf_exempt
# @api_view(['POST'])
# @parser_classes([JSONParser])
# def send_message_to_whatsapp(request, message_id):
#     try:
#         if not User.check_user_token(request.data.get('user_id'), request=request): raise Exception('Not token or user id')
#         message = Messages.objects.get(id=message_id)
#         whats.sendwhatmsg_instantly(message.message_to_number, message.message)
#         return JsonResponse(SUCCESS_MESSAGE)
#     except Exception as error:
#         return JsonResponse(ERROR_MESSAGE(error))