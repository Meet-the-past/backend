from django.contrib import admin

from .models import user

@admin.register(user)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'password', 'is_deleted',
                    'created_at', 'updated_at']
