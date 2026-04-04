from django.db import models
from django.utils.text import slugify

from common.models import TimeStampModel


# Create your models here.
class Faculty(TimeStampModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'unique': 'A faculty with this name already exists.'
        }
    )
    description = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=150)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True
    )

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(f"{self.name}")

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']