from django.http import HttpResponse, JsonResponse
from api.models import User, Categorie
from api.serializers import CategorieSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.views import SUCCESS_MESSAGE, ERROR_MESSAGE

@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def create_categorie(request):
    try:
        if not User.check_user_token(request.data['user_id'], request=request): 
            raise Exception('Invalid token or user_id')
        categorie = Categorie.objects.create(name=request.data['name'], user_id=request.data['user_id'])
        serializer = CategorieSerializer(categorie, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error)) 

def get_categorie(categorie):
    try:
        serializer = CategorieSerializer(categorie, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False)

def update_categorie(request, categorie):
    if request.data.get('name'): categorie.name = request.data.get('name')  
    categorie.save()
    serializer = CategorieSerializer(categorie, many=False)
    return Response(serializer.data)

@csrf_exempt
@api_view(['PUT', 'DELETE', 'GET'])
@parser_classes([JSONParser])
def categorie_details(request, categorie_id):
    try:
        if not User.check_user_token(request.data.get('user_id'), request=request): 
            raise Exception('Invalid token or user_id')

        categorie = Categorie.objects.get(id=categorie_id)

        if request.method == 'DELETE': 
            categorie.delete()
            return JsonResponse(SUCCESS_MESSAGE, safe=False)
        elif request.method == 'GET': 
            return get_categorie(categorie)
        elif request.method == 'PUT':
            return update_categorie(request, categorie)

    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False, status=409)
