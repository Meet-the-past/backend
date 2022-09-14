from django.contrib import admin

from .models import Images


@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['id', 'origin_url', 'converted_url', 'user_id', 'status', 'is_deleted',
                    'created_at', 'updated_at']

# docker-compose exec backend python manage.py createsuperuser
