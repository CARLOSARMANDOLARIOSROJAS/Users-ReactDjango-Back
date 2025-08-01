
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import User

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'age']
        # Removemos password de los campos principales ya que es opcional
    
    def create(self, validated_data):
            # Opción 2: O puedes eliminar el campo password completamente
        validated_data.pop('password', None)
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Solo hacer hash si se proporciona una contraseña y no está vacía
        if 'password' in validated_data and validated_data['password']:
            validated_data['password'] = make_password(validated_data['password'])
        elif 'password' in validated_data and not validated_data['password']:
            # Si password está vacío, no lo actualizamos
            validated_data.pop('password')
        
        return super().update(instance, validated_data)
    
    def validate_username(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está en uso.")
        return value
    
    def validate_email(self, value):
        user_id = self.instance.id if self.instance else None
        if User.objects.exclude(id=user_id).filter(email=value).exists():
            raise serializers.ValidationError("Este correo electrónico ya está en uso.")
        return value

class CustomTokenObtainPairSerializer(serializers.Serializer):
    username = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        password = attrs.get('password')

        if not (username or email):
            raise serializers.ValidationError("Se requiere username o email.")

        if not password:
            raise serializers.ValidationError("Se requiere contraseña.")

        user = None
        if username:
            user = User.objects.filter(username=username).first()
        elif email:
            user = User.objects.filter(email=email).first()

        if user is None or not user.check_password(password):
            raise serializers.ValidationError("Credenciales inválidas.")

        return {'user': user}