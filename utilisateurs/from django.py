from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from utilisateurs.models import User

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('numero_telephone', 'password')}),
        ('Informations personnelles', {'fields': ('nom_complet', 'prenom', 'email', 'lieu_habitation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_telephone', 'nom_complet', 'prenom', 'email', 'lieu_habitation', 'password1', 'password2')}
        ),
    )
    search_fields = ('numero_telephone', 'nom_complet', 'prenom', 'email')
    ordering = ('nom_complet',)

admin.site.register(User, CustomUserAdmin)