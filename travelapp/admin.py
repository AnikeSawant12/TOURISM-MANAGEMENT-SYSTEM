from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import *



class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('cusername','cemail', 'cfname', 'cmname', 'clname', 'cgender','cmobileno','caddress1','caddress2','ccity','cstate','ccountry','cpin', 'is_staff', 'is_active',)
    list_filter = ('cemail', 'is_staff', 'is_active','is_superuser',)

    fieldsets = (
        (None, {'fields': ('cusername','cemail', 'cfname', 'cmname', 'clname', 'cgender','cmobileno','caddress1','caddress2','ccity','cstate','ccountry','cpin')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cusername','cemail', 'cfname', 'cmname', 'clname', 'cgender','cmobileno','caddress1','caddress2','ccity','cstate','ccountry','cpin', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('cemail',)
    ordering = ('cemail',)


admin.site.register(CustomUser, CustomUserAdmin)   


@admin.register(Services)
class PartyAdmin(admin.ModelAdmin):
    list_display = ['id', 'shotelname',  'shotelimg', 'shoteltype', 'slug', 'screated_by', 'supdated_at', 'screated_by']


admin.site.register(Package)
admin.site.register(Booking)
admin.site.register(RemaningReservationPayment)


