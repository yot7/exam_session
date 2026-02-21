from django.db import models
from django.utils.text import slugify
from common.models import TimeStampModel


# Create your models here.
class Major(TimeStampModel):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True, blank=True)

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(f"{self.name}")

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name