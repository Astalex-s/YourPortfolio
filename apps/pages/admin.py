from django.contrib import admin
from .models import (
    SiteSettings, SocialLink, ContactMessage, Certificate,
    Education, WorkExperience, Review,
)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ['name', 'url', 'icon_class', 'order']


class CertificateInline(admin.TabularInline):
    model = Certificate
    extra = 1
    fields = ['name', 'issuer', 'year', 'image', 'url', 'order']


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1
    fields = ['degree', 'institution', 'period', 'description', 'order']


class WorkExperienceInline(admin.TabularInline):
    model = WorkExperience
    extra = 1
    fields = ['position', 'company', 'period', 'description', 'order']


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1
    autocomplete_fields = ['project']
    fields = [
        'author_name', 'author_position', 'project',
        'screenshot', 'text', 'rating', 'review_date',
        'order', 'is_published',
    ]


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    inlines = [SocialLinkInline, CertificateInline, EducationInline, WorkExperienceInline, ReviewInline]
    fieldsets = (
        ('Личная информация', {
            'fields': ('owner_name', 'tagline', 'about_text', 'logo', 'avatar', 'about_photo')
        }),
        ('Контакты', {
            'fields': ('email', 'phone', 'location', 'birth_date')
        }),
        ('Резюме', {
            'fields': ('resume_pdf', 'cv_data'),
            'classes': ('collapse',),
        }),
        ('SEO', {
            'fields': ('meta_description',),
            'classes': ('collapse',),
        }),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'telegram_username', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
    search_fields = ['name', 'email', 'telegram_username', 'subject']
    readonly_fields = ['name', 'email', 'telegram_username', 'subject', 'message', 'created_at']
    list_editable = ['is_read']

    def has_add_permission(self, request):
        return False
