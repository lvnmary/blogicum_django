from django.contrib.auth import get_user_model
from django.db import models

from .constants import (
    MAX_TITLE_LENGTH,
    MAX_POST_NAME_LENGTH,
    MAX_LOCATION_NAME_LENGTH,
    MAX_CATEGORY_NAME_LENGTH,
)

User = get_user_model()


class BaseModel(models.Model):
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True


class Category(BaseModel):
    title = models.CharField(
        max_length=MAX_CATEGORY_NAME_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL; разрешены символы '
                  'латиницы, цифры, дефис и подчёркивание.'
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:MAX_TITLE_LENGTH]


class Location(BaseModel):
    name = models.CharField(
        max_length=MAX_LOCATION_NAME_LENGTH,
        verbose_name='Название места'
    )

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'


class Post(BaseModel):
    title = models.CharField(
        max_length=MAX_POST_NAME_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем — '
                  'можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        related_name='posts',
        null=True,
        blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        null=True,
        related_name='posts',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self):
        return self.title[:MAX_TITLE_LENGTH]
