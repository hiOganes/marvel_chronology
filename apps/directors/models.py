from django.db import models
from django.utils.text import slugify
from unidecode import unidecode


class Directors(models.Model):
    first_name = models.CharField()
    last_name = models.CharField()
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(unidecode(self.full_name))
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name