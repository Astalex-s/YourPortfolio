from django.db import models
from apps.core.models import TimeStampedModel


class SiteSettings(TimeStampedModel):
    owner_name = models.CharField(max_length=100, verbose_name='Имя')
    tagline = models.CharField(max_length=200, verbose_name='Слоган')
    about_text = models.TextField(verbose_name='О себе')
    logo = models.ImageField(
        upload_to='pages/logo/', blank=True, null=True,
        verbose_name='Логотип (шапка и подвал)'
    )
    avatar = models.ImageField(
        upload_to='pages/avatar/', blank=True, null=True,
        verbose_name='Аватар (фото на главной)'
    )
    about_photo = models.ImageField(
        upload_to='pages/about/', blank=True, null=True,
        verbose_name='Фото на странице «Обо мне»'
    )
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=30, blank=True, verbose_name='Телефон')
    location = models.CharField(max_length=100, blank=True, verbose_name='Местоположение')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    resume_pdf = models.FileField(
        upload_to='pages/resume/', blank=True, null=True,
        verbose_name='Резюме PDF'
    )
    cv_data = models.JSONField(default=dict, blank=True, verbose_name='Данные CV (JSON)')
    meta_description = models.CharField(
        max_length=160, blank=True, verbose_name='Meta Description'
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return f'Настройки — {self.owner_name}'

    def save(self, *args, **kwargs):
        # Singleton: only one row allowed
        if not self.pk and SiteSettings.objects.exists():
            existing = SiteSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)


class Certificate(TimeStampedModel):
    site_settings = models.ForeignKey(
        SiteSettings, related_name='certificates',
        on_delete=models.CASCADE, verbose_name='Настройки'
    )
    name   = models.CharField(max_length=200, verbose_name='Название')
    issuer = models.CharField(max_length=100, verbose_name='Выдан')
    year   = models.CharField(max_length=10,  verbose_name='Год')
    image  = models.ImageField(
        upload_to='pages/certificates/', blank=True, null=True,
        verbose_name='Изображение сертификата'
    )
    url    = models.URLField(blank=True, verbose_name='Ссылка (опционально)')
    order  = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'
        ordering = ['order']

    def __str__(self):
        return f'{self.name} — {self.issuer}'


class SocialLink(TimeStampedModel):
    site_settings = models.ForeignKey(
        SiteSettings, related_name='social_links',
        on_delete=models.CASCADE, verbose_name='Настройки'
    )
    name = models.CharField(max_length=50, verbose_name='Название')
    url = models.URLField(verbose_name='URL')
    icon_class = models.CharField(
        max_length=50, verbose_name='CSS класс иконки',
        help_text='Например: fab fa-github'
    )
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Ссылка соцсети'
        verbose_name_plural = 'Ссылки соцсетей'
        ordering = ['order']

    def __str__(self):
        return self.name


class Education(TimeStampedModel):
    site_settings = models.ForeignKey(
        SiteSettings, related_name='educations',
        on_delete=models.CASCADE, verbose_name='Настройки'
    )
    degree = models.CharField(max_length=200, verbose_name='Степень / специальность')
    institution = models.CharField(max_length=200, verbose_name='Учебное заведение')
    period = models.CharField(max_length=50, verbose_name='Период', help_text='Например: 2018 — 2022')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Образование'
        verbose_name_plural = 'Образование'
        ordering = ['order']

    def __str__(self):
        return f'{self.degree} — {self.institution}'


class WorkExperience(TimeStampedModel):
    site_settings = models.ForeignKey(
        SiteSettings, related_name='experiences',
        on_delete=models.CASCADE, verbose_name='Настройки'
    )
    position = models.CharField(max_length=200, verbose_name='Должность')
    company = models.CharField(max_length=200, verbose_name='Компания')
    period = models.CharField(max_length=50, verbose_name='Период', help_text='Например: 2022 — настоящее время')
    description = models.TextField(blank=True, verbose_name='Описание')
    order = models.PositiveSmallIntegerField(default=0, verbose_name='Порядок')

    class Meta:
        verbose_name = 'Опыт работы'
        verbose_name_plural = 'Опыт работы'
        ordering = ['order']

    def __str__(self):
        return f'{self.position} — {self.company}'


class ContactMessage(TimeStampedModel):
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=200, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Входящие сообщения'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'
