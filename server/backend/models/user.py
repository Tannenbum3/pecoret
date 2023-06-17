from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user class with unique emails
    """
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ["username"]

    @property
    def report_display_name(self):
        # pylint: disable=no-member
        if self.usersettings.show_real_name_in_report:
            return f"{self.first_name} {self.last_name}"
        return self.username
