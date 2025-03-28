from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, ProfileCollecteur
from django.utils.translation import gettext_lazy as _

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('nom_complet', 'prenom', 'numero_telephone', 'email', 
                    'lieu_habitation', 'role', 'is_active', 'is_staff', 'has_collector_profile')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('numero_telephone', 'nom_complet', 'prenom', 'email')
    ordering = ('nom_complet',)
    list_per_page = 25
    show_full_result_count = True

    fieldsets = (
        (None, {'fields': ('numero_telephone', 'password')}),
        (_('Informations personnelles'), {
            'fields': ('nom_complet', 'prenom', 'email', 'lieu_habitation')
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 
                      'groups', 'user_permissions', 'role')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('numero_telephone', 'nom_complet', 'prenom', 
                      'email', 'lieu_habitation', 'password1', 
                      'password2', 'role'),
        }),
    )

    actions = ['make_collector', 'remove_collector_status']

    def has_collector_profile(self, obj):
        return hasattr(obj, 'profile_collecteur')
    has_collector_profile.boolean = True
    has_collector_profile.short_description = _('Profil Collecteur')

    def make_collector(self, request, queryset):
        # Vérifier si les utilisateurs ont déjà un profil collecteur
        for user in queryset:
            if not hasattr(user, 'profile_collecteur'):
                self.message_user(
                    request,
                    f"L'utilisateur {user.nom_complet} n'a pas de profil collecteur. Créez-en un d'abord.",
                    level='ERROR'
                )
                return
                
        updated = queryset.update(role='collecteur')
        self.message_user(
            request,
            f"{updated} utilisateur(s) ont été définis comme collecteurs.",
            level='SUCCESS'
        )
    make_collector.short_description = _("Définir comme collecteurs (avec profil existant)")

    def remove_collector_status(self, request, queryset):
        # Vérifier si les utilisateurs ont un profil collecteur
        for user in queryset:
            if hasattr(user, 'profile_collecteur'):
                self.message_user(
                    request,
                    f"L'utilisateur {user.nom_complet} a un profil collecteur. Supprimez-le d'abord.",
                    level='ERROR'
                )
                return
                
        updated = queryset.update(role='client')
        self.message_user(
            request,
            f"{updated} utilisateur(s) ont été définis comme clients.",
            level='SUCCESS'
        )
    remove_collector_status.short_description = _("Définir comme clients (sans profil collecteur)")

    def save_model(self, request, obj, form, change):
        # Lors de la sauvegarde, vérifier la cohérence rôle/profil
        if hasattr(obj, 'profile_collecteur') and obj.role != 'collecteur':
            obj.role = 'collecteur'
        super().save_model(request, obj, form, change)

class ProfileCollecteurAdmin(admin.ModelAdmin):
    list_display = ('user', 'nif', 'stat', 'cin', 'created_at', 'updated_at')
    search_fields = ('user__nom_complet', 'nif', 'stat', 'cin')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    raw_id_fields = ('user',)

    def save_model(self, request, obj, form, change):
        # Lors de la création/mise à jour d'un profil collecteur, mettre à jour le rôle
        obj.user.role = 'collecteur'
        obj.user.save()
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        # Lors de la suppression d'un profil collecteur, vérifier si on doit changer le rôle
        # (Dans notre cas, on laisse le rôle car c'est une suppression)
        super().delete_model(request, obj)

admin.site.register(User, CustomUserAdmin)
admin.site.register(ProfileCollecteur, ProfileCollecteurAdmin)