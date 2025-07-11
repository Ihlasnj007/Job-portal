from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','is_employer','is_jobseeker','is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_jobseeker','is_employer','is_active')
    ordering = ('email',)
    search_fields = ('email',)

    fieldsets = (
        (None, {'fields': ('email','password')}),
        ('permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'is_employer', 'is_jobseeker',
        )}),
        ('Important Dates',{'fields': ('last_login', 'date_joined')})
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',
                        'is_employer', 'is_jobseeker', 'is_active', 'is_staff','is_superuser'),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)
