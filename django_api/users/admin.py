from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    """
    Configuração do painel administrativo para o modelo CustomUser
    """
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_verified', 'created_at')
    list_filter = ('is_active', 'is_verified', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Informações de Acesso', {
            'fields': ('username', 'password', 'email')
        }),
        ('Informações Pessoais', {
            'fields': ('first_name', 'last_name', 'phone', 'bio', 'avatar')
        }),
        ('Permissões e Status', {
            'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at', 'last_login'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ('-created_at',)
