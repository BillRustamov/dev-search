import uuid

from django.db import models
from django.contrib.auth import get_user_model

Profile = get_user_model()


class Project(models.Model):
    # ForeignKey == OneToMany
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True)  # unique=True
    description = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='project-photos/',
                              default='devsearch-test/project-photos/project-default.jpg', null=True,
                              blank=True)
    source_code = models.URLField(null=True, blank=True)
    live_demo = models.URLField(null=True, blank=True)
    tags = models.ManyToManyField(to='Tag')
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=255)
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    owner = models.ForeignKey(to=Profile, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Ulugbek Umaraliyev - Consectetur adipisicing elit. Re...
        return f'{self.owner} - {self.body[:25]}...'

