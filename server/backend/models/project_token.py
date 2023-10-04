from django.db import models


class ProjectTokenManager(models.Manager):
    def for_project(self, project):
        return self.get_queryset().filter(project=project)
