from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from rest_framework_jwt.settings import api_settings
# Create your models here.

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserManager(BaseUserManager):
    """Inherits BaseUserManager class for Django Super Admin"""

    def create_superuser(self, email, password):
        """Creates and saves a  Django superuser"""
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    first_name = models.CharField("First Name", max_length=100)
    middle_name = models.CharField("Middle Name", max_length=100, blank=True, null=True)
    last_name = models.CharField("Last Name", max_length=100)
    full_name = models.CharField("Full Name", max_length=100, blank=True, null=True)
    mobile = models.CharField('Mobile Number', max_length=10, null=True, blank=True)
    follow = models.ManyToManyField('self',related_name='follow_to',default=[])
    is_staff = models.BooleanField('Staff', default=False)
    is_active = models.BooleanField('Is Active', default=False)
    created_datetime = models.DateTimeField("Created date", auto_now_add=True)
    updated_datetime = models.DateTimeField("Updated date", auto_now=True)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        get_latest_by = ['id']

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        if self.middle_name:
            return "{} {} {}".format(self.first_name, self.middle_name, self.last_name)
        return "{} {}".format(self.first_name, self.last_name)

    def save(self, *args, **kwargs):
        self.email = self.email.lower()
        self.full_name = self.get_full_name()
        super(User, self).save(*args, **kwargs)

    def create_jwt(self):
        """ Generating JWT Token for Authentication"""

        payload = jwt_payload_handler(self)
        token = jwt_encode_handler(payload)
        return token

    def token(self):
        return self.create_jwt()
