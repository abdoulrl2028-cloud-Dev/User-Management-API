from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def api_root(request):
    """
    Retorna informações sobre a API
    """
    return Response({
        'message': 'Bem-vindo à User Management API',
        'version': '1.0.0',
        'endpoints': {
            'usuarios': '/api/users/',
            'meu_perfil': '/api/users/me/',
            'docs': '/admin/'
        }
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api_root),
    path('api/', include('users.urls')),
    path('api-auth/', include('rest_framework.urls')),
]
