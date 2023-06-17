import secrets
from django.utils import timezone
from django.db import models


class ProjectTokenManager(models.Manager):
    def for_project(self, project):
        return self.get_queryset().filter(project=project)


class ProjectToken(models.Model):
    TOKEN_LENGTH = 72

    objects = ProjectTokenManager()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    project = models.ForeignKey('backend.Project', on_delete=models.CASCADE)
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    date_expire = models.DateTimeField()
    key = models.CharField(max_length=512, primary_key=True, editable=False)
    name = models.CharField(max_length=32)

    @classmethod
    def generate_key(cls):
        return secrets.token_hex(cls.TOKEN_LENGTH)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date_expire"]
        verbose_name = "Project Token"
        verbose_name_plural = "Project Tokens"

    def is_expired(self):
        return timezone.now() >= self.date_expire
