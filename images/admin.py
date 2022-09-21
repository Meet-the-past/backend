from django.contrib import admin

from .models import images


@admin.register(images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'origin_url', 'converted_url',  'is_deleted',
                    'created_at', 'updated_at']#'user_id', 'status',

# docker-compose exec backend python manage.py createsuperuser
