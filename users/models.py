import uuid
import datetime

from django.db import models

from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)


class ProfileManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, *args, **kwargs):
        if not email:
            raise ValueError("Profile should have an email field value")
        if not first_name:
            raise ValueError("Profile should have a first_name field value")
        if not last_name:
            raise ValueError("Profile should have a last_name field value")
        email = self.normalize_email(email=email)
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            *args,
            **kwargs
        )
        user.set_password(raw_password=password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, first_name, last_name, password, *args, **kwargs):
        superuser = self.create_user(email=email, first_name=first_name, last_name=last_name, password=password, *args,
                                     **kwargs)
        superuser.is_superuser = True
        superuser.is_staff = True

        superuser.save(using=self._db)


class Profile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='profile-avatars/', default='devsearch-test/profile-avatars/user-default.png',
                              null=True,
                              blank=True)
    short_intro = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    social_instagram = models.URLField(null=True, blank=True)
    social_facebook = models.URLField(null=True, blank=True)
    social_website = models.URLField(null=True, blank=True)
    social_github = models.URLField(null=True, blank=True)
    social_linkedin = models.URLField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ProfileManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_username(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def get_email(self):
        return self.email

    @property
    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name


class Skill(models.Model):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        fullname = self.profile.get_full_name
        return f'{self.name} - {fullname}'


class Message(models.Model):
    sender = models.ForeignKey(to=Profile, on_delete=models.SET_NULL,
                               null=True, blank=True,
                               related_name='sent_messages')
    recipient = models.ForeignKey(to=Profile,
                                  on_delete=models.CASCADE,
                                  related_name='received_messages')

    fullname = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)
    subject = models.CharField(max_length=200)
    body = models.TextField()
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f"{self.sender} - {self.recipient} - {self.subject}"
