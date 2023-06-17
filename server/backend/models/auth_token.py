import secrets
from django.utils import timezone
from django.db import models


class AuthToken(models.Model):
    TOKEN_LENGTH = 42

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('backend.User', on_delete=models.CASCADE)
    date_expire = models.DateTimeField()
    key = models.CharField(max_length=512, primary_key=True, editable=False)

    @classmethod
    def generate_key(cls):
        return secrets.token_hex(cls.TOKEN_LENGTH)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
            self.date_expire = timezone.now() + timezone.timedelta(hours=20)
        return super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date_expire"]
        verbose_name = "Auth Token"
        verbose_name_plural = "Auth Tokens"

    def is_expired(self):
        return timezone.now() >= self.date_expire
