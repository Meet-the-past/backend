import uuid

from django.db import models

from users.models import user
from django.utils import timezone

class images(models.Model):  ##S
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)# PK 
    origin_url = models.CharField(max_length=200, null = True)
    converted_url = models.CharField(max_length=200,null=True)
    #user_id = models.ForeignKey(user, on_delete=models.CASCADE, db_column='user_id')
    #status = models.TextChoices('status', 'a b c') # Status 입력 셀러리의 상태에 대한 status
    CLEREY_STATUS = (
        ('SUCCESS', 'SUCCESS'),
        ('FAIL', 'FAIL'),
        ('Proceeding', 'Proceeding')
    )

    status = models.CharField(
        max_length=15,
        choices=CLEREY_STATUS,
        blank=True,
        default='FAIL',
        help_text='celery_status',
    )


    is_deleted = models.BooleanField(default=False, null=False)
    #BaseEntity
    created_at = models.DateTimeField(auto_now_add=True,null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        return self.origin_url

    class Meta:
        db_table = 'images'
