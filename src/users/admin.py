from django.contrib import admin
from .models import CustomUser
from django.utils.translation import gettext_lazy as _
from django.apps import apps


# get some specific app
app = apps.get_app_config('graphql_auth')
for model_name, model in app.models.items():
    admin.site.register(model)


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_superuser']

admin.site.register(CustomUser, UserAdmin)
