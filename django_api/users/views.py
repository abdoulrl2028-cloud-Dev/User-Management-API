from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import check_password
from .models import CustomUser
from .serializers import (
    UserSerializer,
    UserCreateSerializer,
    UserUpdateSerializer,
    ChangePasswordSerializer
)
from .permissions import IsOwnerOrReadOnly, IsAuthenticatedOrCreate


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciar usuários
    """
    queryset = CustomUser.objects.all()
    permission_classes = [IsAuthenticatedOrCreate]

    def get_serializer_class(self):
        """
        Retorna o serializer apropriado baseado na ação
        """
        if self.action == 'create':
            return UserCreateSerializer
        elif self.action in ['partial_update', 'update']:
            return UserUpdateSerializer
        elif self.action == 'change_password':
            return ChangePasswordSerializer
        return UserSerializer

    def get_permissions(self):
        """
        Define permissões baseadas na ação
        """
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        elif self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
        
        return [permission() for permission in permission_classes]

    def get_object(self):
        """
        Retorna o objeto do usuário
        """
        obj = super().get_object()
        self.check_object_permissions(self.request, obj)
        return obj

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        Retorna os dados do usuário autenticado
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request, pk=None):
        """
        Permite ao usuário alterar sua senha
        """
        user = self.get_object()
        
        if user != request.user:
            return Response(
                {'detail': 'Você só pode alterar sua própria senha.'},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Verificar se a senha antiga está correta
        if not check_password(serializer.validated_data['old_password'], user.password):
            return Response(
                {'old_password': 'Senha antiga incorreta.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Alterar a senha
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({
            'detail': 'Senha alterada com sucesso.'
        }, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def deactivate(self, request, pk=None):
        """
        Desativa a conta do usuário
        """
        user = self.get_object()
        
        if user != request.user:
            return Response(
                {'detail': 'Você só pode desativar sua própria conta.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.is_active = False
        user.save()

        return Response({
            'detail': 'Conta desativada com sucesso.'
        }, status=status.HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        """
        Lista todos os usuários ativos
        """
        self.queryset = CustomUser.objects.filter(is_active=True)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        Deleta o usuário
        """
        user = self.get_object()
        
        if user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'Você só pode deletar sua própria conta.'},
                status=status.HTTP_403_FORBIDDEN
            )

        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
