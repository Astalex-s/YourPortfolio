from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, mark_safe
from .models import Project, ProjectScreenshot, TechTag


@admin.register(TechTag)
class TechTagAdmin(admin.ModelAdmin):
    list_display = ['name', 'logo_key', 'colored_badge', 'project_count', 'delete_btn']
    search_fields = ['name']
    actions = ['delete_selected']

    def colored_badge(self, obj):
        return format_html(
            '<span style="background:{};color:#fff;padding:2px 8px;border-radius:4px">{}</span>',
            obj.color, obj.name
        )
    colored_badge.short_description = 'Бейдж'

    def project_count(self, obj):
        return obj.projects.filter(is_published=True).count()
    project_count.short_description = 'Проектов'

    def delete_btn(self, obj):
        url = reverse('admin:portfolio_techtag_delete', args=[obj.pk])
        return format_html(
            '<a href="{}" style="color:#e74c3c;font-weight:600;">Удалить</a>', url
        )
    delete_btn.short_description = ''

    def has_delete_permission(self, request, obj=None):
        return True


class ProjectScreenshotInline(admin.TabularInline):
    model = ProjectScreenshot
    extra = 1
    fields = ['image', 'caption', 'order']


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'is_published', 'is_featured', 'order',
        'tech_stack_display', 'created_at'
    ]
    list_filter = ['is_published', 'is_featured', 'tech_stack']
    list_editable = ['is_published', 'is_featured', 'order']
    search_fields = ['title', 'brief_description']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tech_stack']
    inlines = [ProjectScreenshotInline]
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'mockup_image', 'brief_description')
        }),
        ('Детали проекта', {
            'fields': ('task_description', 'how_it_works', 'solution_description', 'result_description')
        }),
        ('Медиа', {
            'fields': ('demo_video_url', 'demo_video_file'),
            'classes': ('collapse',),
        }),
        ('Ссылки', {
            'fields': ('source_link', 'live_demo_link')
        }),
        ('Технологии', {
            'fields': ('tech_stack',)
        }),
        ('Настройки отображения', {
            'fields': ('order', 'is_featured', 'is_published')
        }),
    )

    def tech_stack_display(self, obj):
        tags = obj.tech_stack.all()[:4]
        html = ' '.join(
            f'<span style="background:{t.color};color:#fff;padding:1px 6px;'
            f'border-radius:3px;font-size:11px">{t.name}</span>'
            for t in tags
        )
        return mark_safe(html) if html else '—'
    tech_stack_display.short_description = 'Стек'
