from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class TechTag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Название')
    color = models.CharField(
        max_length=7, default='#4A90D9', verbose_name='Цвет',
        help_text='HEX цвет, например #4A90D9'
    )
    logo_key = models.CharField(
        max_length=50, blank=True, verbose_name='Ключ иконки',
        help_text=(
            'Slug для simpleicons.org. Примеры: python, django, fastapi, flask, '
            'git, postgresql, docker, nginx, vite, telegram, googlesheets, n8n, '
            'javascript, html5, css3'
        )
    )

    class Meta:
        verbose_name = 'Тег технологии'
        verbose_name_plural = 'Теги технологий'
        ordering = ['name']

    def __str__(self):
        return self.name


class Project(TimeStampedModel):
    title = models.CharField(max_length=200, verbose_name='Название проекта')
    slug = models.SlugField(max_length=200, unique=True, blank=True, verbose_name='Slug')
    mockup_image = models.ImageField(
        upload_to='portfolio/mockups/', verbose_name='Мокап (обложка)'
    )
    brief_description = models.CharField(
        max_length=300, verbose_name='Краткое описание'
    )
    task_description = models.TextField(verbose_name='Задача')
    how_it_works = models.TextField(blank=True, verbose_name='Как работает')
    solution_description = models.TextField(verbose_name='Решение')
    result_description = models.TextField(verbose_name='Результат')
    demo_video_url = models.URLField(
        blank=True, verbose_name='Ссылка на видео',
        help_text='YouTube или Vimeo embed URL'
    )
    demo_video_file = models.FileField(
        upload_to='portfolio/videos/', blank=True, null=True,
        verbose_name='Видео файл'
    )
    source_link = models.URLField(blank=True, verbose_name='Ссылка на исходники')
    live_demo_link = models.URLField(blank=True, verbose_name='Ссылка на демо')
    tech_stack = models.ManyToManyField(
        TechTag, blank=True, related_name='projects',
        verbose_name='Технологии'
    )
    order = models.PositiveSmallIntegerField(
        default=0, db_index=True, verbose_name='Порядок'
    )
    is_featured = models.BooleanField(default=False, verbose_name='Избранный')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('portfolio:detail', kwargs={'slug': self.slug})


class ProjectScreenshot(TimeStampedModel):
    project = models.ForeignKey(
        Project, related_name='screenshots',
        on_delete=models.CASCADE, verbose_name='Проект'
    )
    image = models.ImageField(
        upload_to='portfolio/screenshots/', verbose_name='Скриншот'
    )
    caption = models.CharField(
        max_length=200, blank=True, verbose_name='Подпись'
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Скриншот проекта'
        verbose_name_plural = 'Скриншоты проекта'
        ordering = ['order']

    def __str__(self):
        return f'Screenshot #{self.order} — {self.project.title}'
