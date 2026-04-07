from django.db import models
from django.utils.text import slugify
from common.models import TimeStampModel


# Create your models here.
class Major(TimeStampModel):
    name = models.CharField(
        max_length=50,
        unique=True,
        error_messages={
            'unique': 'A major with this name already exists.'
        }
    )
    description = models.TextField(blank=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=True
    )
    faculty = models.ForeignKey(
        'faculties.Faculty',
        on_delete=models.CASCADE,
        related_name='majors',
    )

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            base_slug = slugify(f"{self.name}")
            slug = base_slug
            counter = 1
            while Major.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)


    def __str__(self):
        return self.name