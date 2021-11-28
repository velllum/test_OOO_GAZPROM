from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from slugify import slugify


class Article(models.Model):
    """- Статьи"""
    objects = None
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    description = models.CharField(max_length=255, verbose_name='Описание')
    content = models.TextField(verbose_name='Содержание')
    slug = models.SlugField(unique=True, verbose_name='Ссылка')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_date = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    def get_absolute_url(self):
        """- получить url ..."""
        kwargs = {'slug': self.slug}
        return reverse('', kwargs=kwargs)

    def save(self, *args, **kwargs):
        """- переопределяем сохранение, свойства slug"""
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"<{self.title}>, <{self.author}>"

    class Meta:
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
