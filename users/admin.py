from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'email',
        'id',
        'is_superuser',
        'is_active',
        'date_joined',
        'last_login',
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        # (_('Personal info'), {
        #     'fields': ('first_name', 'last_name'),
        # }),
        (_('Permissions'), {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                # 'groups',
                # 'user_permissions',
            ),
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
        }),
    )
    readonly_fields = ('last_login', 'date_joined', 'id')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email', 'id')
