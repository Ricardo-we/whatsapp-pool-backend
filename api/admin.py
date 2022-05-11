from django.contrib import admin
from .models import User, Categorie, Messages
# Register your models here.

admin.site.register(User)
admin.site.register(Categorie)
admin.site.register(Messages)