from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Utilisateurs, ProfileCollecteur

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('nom_complet', 'prenom', 'numero_telephone', 'email', 'lieu_habitation', 'role', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('numero_telephone', 'password')}),
        ('Informations personnelles', {'fields': ('nom_complet', 'prenom', 'email', 'lieu_habitation')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    # Exclude username field from add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_telephone', 'nom_complet', 'prenom', 'email', 'lieu_habitation', 'password1', 'password2'),
        }),
    )
    search_fields = ('numero_telephone', 'nom_complet', 'prenom', 'email')
    ordering = ('nom_complet',)
    list_per_page = 25
    show_full_result_count = True

class ProfileCollecteurAdmin(admin.ModelAdmin):
    list_display = ('user', 'nif', 'stat', 'cin', 'created_at', 'updated_at')
    search_fields = ('user__nom_complet', 'nif', 'stat', 'cin')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(ProfileCollecteur, ProfileCollecteurAdmin)
