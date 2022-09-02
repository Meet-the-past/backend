import uuid

from django.db import models

from users.models import user


class Images(models.Model):  ##S
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)# PK

    origin_url = models.CharField(max_length=200)
    converted_url = models.CharField(max_length=200)
    user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column='user_id')
    status = models.TextChoices('status', 'a b c') # Status 입력
    is_deleted = models.BooleanField(default=False, null=False)

    #BaseEntity
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.textfield

    class Meta:
        db_table = 'image'
