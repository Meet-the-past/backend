import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


class user(models.Model): # 상속 클래스 내용으로 인한 error
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)  # PK
    name = models.CharField(max_length=200, null=False)
    email = models.CharField(max_length=50)
    # email = models.EmailField(_('email address'), unique=False)
    password = models.BinaryField(max_length=60)
    # password = models.CharField(max_length=200, null=False)
    is_deleted = models.BooleanField(default=False, null=False)
    salt = models.BinaryField(max_length=29)

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
    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False    
    class Meta:
        db_table = 'user'
