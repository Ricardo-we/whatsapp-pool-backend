from django.db import models
from uuid import uuid4

# Create your models here.


def generate_auth_token(users):
    token = uuid4()
    all_users = users.objects.all()
    current_user = 0
    while current_user < len(all_users):
        if token == all_users[current_user].auth_token:
            token = uuid4()
            current_user = 0
        current_user += 1
    return token


class User(models.Model):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=300, null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    password = models.CharField(max_length=255)
    auth_token = models.CharField(max_length=255, unique=True)

    @staticmethod
    def create_user(username, password, email, phone_number):
        try:

            required_msg = " is required"
            validation_messages = {
                "username": "Username" + required_msg,
                "password": "Password" + required_msg,
                "email": "Email" + required_msg
            }

            if not username or not email or not password:
                if not username:
                    required_field = "username"
                elif not password:
                    required_field = "password"
                else:
                    required_field = "email"
                raise Exception(validation_messages[required_field])

            user = User.objects.create(
                username=username,
                password=password,
                phone_number=phone_number,
                email=email,
                auth_token=generate_auth_token(User)
            )
            return user
        except Exception as error:
            print(error)
            return Exception(str(error))

    @staticmethod
    def check_user_token(user_id, token='', request=None, returning=False):
        token_ = token
        user__id = user_id
        if request:
            token_ = request.headers.get('Authorization')
        if not user_id and request:
            user__id = request.GET.get('user_id')

        if returning:
            return User.objects.get(id=user__id, auth_token=token_)
        return True if User.objects.get(id=user__id, auth_token=token_) else False


class Categorie(models.Model):
    user = models.ForeignKey(User, related_name="user_categorie", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)


class Messages(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    message_to = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=400, null=True, blank=True)
    message_interval = models.CharField(max_length=255, null=True, blank=True)
    message_type = models.CharField(max_length=255, default="email")
    message = models.TextField()
