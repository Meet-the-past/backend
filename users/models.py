import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class user(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)  # PK
    name = models.CharField(max_length=200, null=False)
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(max_length=200, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    # BaseEntity
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    spouse_name = models.CharField(blank=True, max_length=100)
    date_of_birth = models.DateField(blank=True, null=True)
    def __str__(self):
        return self.email
    class Meta:
        db_table = 'user'
