import uuid

from django.db import models

from users.models import user
from django.utils import timezone

class images(models.Model):  ##S
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)# PK
   

    origin_url = models.CharField(max_length=200)
    converted_url = models.CharField(max_length=200,null=True)
    #user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column='user_id')
    status = models.TextChoices('status', 'a b c') # Status 입력
    # LOAN_STATUS = (
    #     ('m', 'Maintenance'),
    #     ('o', 'On loan'),
    #     ('a', 'Available'),
    #     ('r', 'Reserved'),
    # )

    # status = models.CharField(
    #     max_length=1,
    #     choices=LOAN_STATUS,
    #     blank=True,
    #     default='m',
    #     help_text='Book availability',
    # )


    is_deleted = models.BooleanField(default=False, null=False)
    #BaseEntity
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.origin_url

    class Meta:
        db_table = 'images'
