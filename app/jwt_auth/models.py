from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models

# Create your models here.

class Role(models.Model):
    role_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "権限"
        verbose_name_plural = "権限管理"
    
class UserInfo(models.Model):
    name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    name_furi = models.CharField(max_length=50, blank=True, null=True)
    last_name_furi = models.CharField(max_length=50, blank=True, null=True)
    first_name_furi = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)

    role = models.ForeignKey(Role, on_delete=models.CASCADE, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ユーザー情報"
        verbose_name_plural = "ユーザー情報管理"


class User(AbstractUser):
    user_id = models.CharField(max_length=50, null=True, blank=True)
    user_info = models.ForeignKey(UserInfo, on_delete=models.CASCADE, blank=True, null=True)

    username = None
    last_name = None
    first_name = None
    email = models.EmailField(_('email address'), unique=True)
    REQUIRED_FIELDS=[]

    USERNAME_FIELD = 'email'

    PERMISSION_CHOICES = [
        ("super", 'Site Manager'),
        ("customer", 'Customer Company'),
    ]
    permission = models.CharField(max_length=50, choices=PERMISSION_CHOICES, default="customer")

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "ユーザー"
        verbose_name_plural = "ユーザー管理"

class RegisterToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    expire_at = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=1024)
    expire_at = models.DateTimeField()

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Email(models.Model):

    when = models.DateTimeField(null=False, auto_now_add=True)
    to = models.EmailField(null=False, blank=False,)
    subject = models.CharField(null=False, max_length=128,)
    body = models.TextField(null=False, max_length=1024,)
    ok = models.BooleanField(null=False, default=True,)
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "メール"
        verbose_name_plural = "メール管理"