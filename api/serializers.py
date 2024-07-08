# from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from .models import User, Organisation
from rest_framework import serializers
class OrgSerializer(ModelSerializer):
    # user=serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)
    class Meta:
        model=Organisation
        fields=( 'id', 'name', 'description')
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=('id', 'first_name', 'last_name', 'email', 'phone', 'password') 
        required_fields=('id', 'first_name', 'last_name', 'email', 'phone', 'password')
        extra_kwargs={
            'password':{'write_only':True},
        }
    def create(self, validated_data):
        try:   
            password=validated_data.pop('password')
            user=User.objects.create(**validated_data)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            print(f'error occurred {e}')

class LoginSerializer(ModelSerializer):
    class Meta:
        model=User
        fields=('email', 'password')
        def create(self, data):
            pass
             
        
        

