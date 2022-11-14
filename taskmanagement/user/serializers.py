from django.contrib.auth import get_user_model
from rest_framework import serializers
User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password','user_permissions','groups']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        #exclude = ['password','groups','user_permissions']
        fields = ('id','email','full_name','is_active','follow','token')



    