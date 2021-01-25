from rest_framework            import serializers
from rest_framework.exceptions import ValidationError

from .models                   import User
from .utils                    import validate_password

class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model  = User
        fields = ['name', 'email', 'password', 'phone_number', 'is_location_agreed', 'is_promotion_agreed']

    def validate_password(self, value):
        if not validate_password(value):
            raise serializers.ValidationError('Invalid password format')
        return value

    def validate_name(self, value):
        if len(value) < 2:
            raise serializers.ValidationError('Too short name')
        return value

class UserSerializer(serializers.Serializer):
    email    = serializers.EmailField(max_length=100)
    password = serializers.CharField(max_length=250)
