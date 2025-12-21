from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para listar usuários
    """
    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone', 'bio', 'avatar', 'is_active', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Serializer para criação de usuários com validação de senha
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password', 'password2',
            'first_name', 'last_name', 'phone'
        ]

    def validate(self, attrs):
        """
        Validar se as senhas são iguais
        """
        if attrs['password'] != attrs.pop('password2'):
            raise serializers.ValidationError({
                'password': 'As senhas não correspondem.'
            })
        return attrs

    def create(self, validated_data):
        """
        Criar novo usuário com senha criptografada
        """
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', '')
        )
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer para atualizar dados do usuário
    """
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'phone', 'bio', 'avatar'
        ]


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer para alterar senha do usuário
    """
    old_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """
        Validar se as novas senhas são iguais
        """
        if attrs['new_password'] != attrs.pop('new_password2'):
            raise serializers.ValidationError({
                'new_password': 'As senhas não correspondem.'
            })
        return attrs
