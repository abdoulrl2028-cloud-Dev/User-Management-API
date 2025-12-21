from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Permissão customizada que permite que apenas o owner edite seu próprio objeto.
    """
    def has_object_permission(self, request, view, obj):
        # Leitura é permitida para qualquer um
        if request.method in SAFE_METHODS:
            return True

        # Escrita apenas para o owner
        return obj == request.user


class IsAuthenticatedOrCreate(BasePermission):
    """
    Permissão que permite criar usuários sem autenticação,
    mas protege outras ações.
    """
    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        if request.user and request.user.is_authenticated:
            return True
        return False
