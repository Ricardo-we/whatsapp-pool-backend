from .models import User, Categorie, Messages
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = User
        fields = '__all__'

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class MessagesSerializer(serializers.ModelSerializer):
    categorie_name = serializers.SerializerMethodField('categorie__name')
    
    class Meta:
        model = Messages
        fields = '__all__'

    def categorie__name(self, obj):
        try:
            return obj.categorie.name    
        except: 
            return 'Not categorie'
