from django.urls import path
from .routes.users import delete_account, login, sign_up, users_updates, get_user_messages, get_user_categories, delete_account
from .routes.categories import create_categorie, categorie_details
from .routes.messages import create_message, message_details

USERS_ENDPOINT = 'users'
CATEGORIES_ENDPOINT = 'categories'
MESSAGES_ENDPOINT = 'messages'

urlpatterns = [
    path(f'{USERS_ENDPOINT}/login', login),
    path(f'{USERS_ENDPOINT}/sign-up', sign_up),
    path(f'{USERS_ENDPOINT}/<int:pk>', users_updates),
    path(f'{USERS_ENDPOINT}/<int:user_id>/categories', get_user_categories),
    path(f'{USERS_ENDPOINT}/<int:user_id>/messages', get_user_messages),
    # DELETE ACCOUNT WITH URL
    path(f'{USERS_ENDPOINT}/delete-account', delete_account),
    # path(f'{ENDPOINT}', get_users),

    # CATEGORIES
    path(f'{CATEGORIES_ENDPOINT}', create_categorie),
    path(f'{CATEGORIES_ENDPOINT}/<int:categorie_id>', categorie_details),

    # MESSAGES
    path(f'{MESSAGES_ENDPOINT}', create_message),
    path(f'{MESSAGES_ENDPOINT}/<int:message_id>', message_details),
    # path(f'{MESSAGES_ENDPOINT}/<int:message_id>/send', send_message_to_whatsapp),
]
