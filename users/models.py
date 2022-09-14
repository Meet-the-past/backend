import uuid

from django.db import models


class user(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)  # PK

    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(max_length=128, null=False)
    password = models.CharField(max_length=200, null=False)

    is_deleted = models.BooleanField(default=False, null=False)

    # BaseEntity
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    class Meta:
        db_table = 'users'
