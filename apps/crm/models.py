from django.db import models
from apps.core.models import TimeStampedModel


class Client(TimeStampedModel):
    name = models.CharField(max_length=200, verbose_name='Имя / Компания')
    email = models.EmailField(blank=True, verbose_name='Email')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    company = models.CharField(max_length=200, blank=True, verbose_name='Организация')
    source = models.CharField(
        max_length=100, blank=True, verbose_name='Источник',
        help_text='Откуда пришёл клиент (hh.ru, LinkedIn, Telegram и т.д.)'
    )
    notes = models.TextField(blank=True, verbose_name='Заметки')
    is_active = models.BooleanField(default=True, verbose_name='Активный')

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class ClientTask(TimeStampedModel):
    STATUS_TODO = 'todo'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_DONE = 'done'
    STATUS_CANCELLED = 'cancelled'
    STATUS_CHOICES = [
        (STATUS_TODO, 'К выполнению'),
        (STATUS_IN_PROGRESS, 'В работе'),
        (STATUS_DONE, 'Выполнено'),
        (STATUS_CANCELLED, 'Отменено'),
    ]

    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, 'Низкий'),
        (PRIORITY_MEDIUM, 'Средний'),
        (PRIORITY_HIGH, 'Высокий'),
    ]

    client = models.ForeignKey(
        Client, related_name='tasks', on_delete=models.CASCADE,
        verbose_name='Клиент'
    )
    title = models.CharField(max_length=300, verbose_name='Задача')
    description = models.TextField(blank=True, verbose_name='Описание')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default=STATUS_TODO, verbose_name='Статус'
    )
    priority = models.CharField(
        max_length=10, choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM, verbose_name='Приоритет'
    )
    due_date = models.DateField(null=True, blank=True, verbose_name='Срок')
    estimated_hours = models.DecimalField(
        max_digits=6, decimal_places=2,
        null=True, blank=True, verbose_name='Оценка (ч)'
    )

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.client.name} — {self.title}'


class WorkLog(TimeStampedModel):
    task = models.ForeignKey(
        ClientTask, related_name='logs', on_delete=models.CASCADE,
        verbose_name='Задача'
    )
    date = models.DateField(verbose_name='Дата')
    hours = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Часы'
    )
    description = models.TextField(blank=True, verbose_name='Что сделано')

    class Meta:
        verbose_name = 'Лог работы'
        verbose_name_plural = 'Логи работы'
        ordering = ['-date']

    def __str__(self):
        return f'{self.date} — {self.hours}ч — {self.task.title}'


class LearningNote(TimeStampedModel):
    CATEGORY_CHOICES = [
        ('tech', 'Технология'),
        ('framework', 'Фреймворк'),
        ('pattern', 'Паттерн'),
        ('tool', 'Инструмент'),
        ('other', 'Другое'),
    ]

    title = models.CharField(max_length=300, verbose_name='Тема')
    content = models.TextField(verbose_name='Заметка')
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES,
        default='tech', verbose_name='Категория'
    )
    tags = models.CharField(
        max_length=300, blank=True, verbose_name='Теги',
        help_text='Через запятую: python, django, celery'
    )
    source_url = models.URLField(blank=True, verbose_name='Источник')
    is_important = models.BooleanField(default=False, verbose_name='Важная')

    class Meta:
        verbose_name = 'Учебная заметка'
        verbose_name_plural = 'Учебные заметки'
        ordering = ['-created_at']

    def __str__(self):
        return self.title
