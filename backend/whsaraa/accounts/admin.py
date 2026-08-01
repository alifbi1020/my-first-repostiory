from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import user


class CustomUserAdmin(UserAdmin):
    model = user
    list_display = ('membership_code', 'national_code', 'first_name', 'last_name', 'phone_number', 'is_staff')

    fieldsets = UserAdmin.fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('national_code', 'membership_code', 'phone_number')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('اطلاعات تکمیلی', {'fields': ('national_code', 'membership_code', 'phone_number')}),
    )


admin.site.register(user, CustomUserAdmin)