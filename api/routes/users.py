from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from api.models import Messages, User, Categorie
from api.serializers import MessagesSerializer, UserSerializer, CategorieSerializer 
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from api.views import SUCCESS_MESSAGE, ERROR_MESSAGE
from django.core.mail import send_mail
from django.conf import settings

def mail_template(user):
    send_mail(
        'Whatssapp pool',
        f'''
            Welcome to whatsapp pool app {user.username}, did you register?
            if you didnt register with this email please desactivate it with this link
            {settings.HOST_URL}/api/users/delete-account?user_id={user.id}&auth_token={user.auth_token}
        ''',
        settings.EMAIL_HOST_USER,
        [user.email]
    )

def validate_phone_number(phone=''):
    try:
        if phone is None: return None
        phone_ = phone.replace(' ', '').replace('-', '')
        if not '+' in phone: phone_ = '+' + phone_
        phone_is_int = int(phone_.split('+')[1])
        if len(phone_) < 16 and len(phone_) > 7:
            return phone_
    except:
        raise Exception('Invalid phone number')

@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def login(request):
    try:
        username_or_email = request.data.get('username')
        password = request.data['password']
        
        if '@' in username_or_email: user = User.objects.filter(email=username_or_email, password=password).first()
        else: user = User.objects.get(username=username_or_email, password=password)

        serializer = UserSerializer(user, many=False)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False)

@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def sign_up(request):
    try:
        email = request.data['email']
        username= request.data['username']
        password = request.data['password']
        phone_number = validate_phone_number(request.data.get('phone_number').strip())
        user = User.create_user(username, password, email, phone_number)
        serializer = UserSerializer(user, many=False)
        if not user: raise Exception('Error creating user')

        mail_template(user)
        return Response(serializer.data)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False)

def update_user(request, user):
    if request.data.get('username'): user.username = request.data['username']
    if request.data.get('password'): user.password = request.data['password']
    if request.data.get('phone_number'): user.phone_number = validate_phone_number(request.data['phone_number'])
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@csrf_exempt
@api_view(['PUT', 'DELETE'])
@parser_classes([JSONParser])
def users_updates(request, pk=0):
    try:
        user = User.objects.get(id=pk)

        print(pk, request.headers.get('Authorization'))
        if not User.check_user_token(pk, None, request): raise Exception('User token or user.id invalid')

        if request.method == 'PUT':
            return update_user(request, user)
        elif request.method == 'DELETE':
            user.delete()
            return Response(SUCCESS_MESSAGE)
    except Exception as error:
        return JsonResponse(ERROR_MESSAGE(error), safe=False) 


# EXTRAS, "SPECIAL URLS"
@csrf_exempt
@api_view(['GET'])
@parser_classes([JSONParser])
def get_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def delete_account(request):
    try:
        user_id = request.GET.get('user_id')
        auth_token = request.GET.get('auth_token')
        if not User.check_user_token(user_id, auth_token): 
            return HttpResponse('<h1>Invalid credentials</h1>',status=400)
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect(f'{settings.CLIENT_URL}/logout')
    except Exception as err:
        print(err) 
        return HttpResponse('<h2>Something went wrong</h2>', status=500)


# EXTRA: RELATIONSHIP URLS
@csrf_exempt
@api_view(['GET'])
def get_user_categories(request, user_id):
    user_categories = Categorie.objects.filter(user__id=user_id).all()
    serializer = CategorieSerializer(user_categories, many=True)
    return Response(serializer.data)

@csrf_exempt
@api_view(['GET'])
def get_user_messages(request, user_id):
    user_messages = Messages.objects.filter(user__id=user_id).all().order_by('categorie__name')
    serializer = MessagesSerializer(user_messages, many=True)
    return Response(serializer.data)
