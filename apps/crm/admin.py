from django.contrib import admin
from django.db.models import Sum
from .models import Client, ClientTask, WorkLog, LearningNote


class WorkLogInline(admin.TabularInline):
    model = WorkLog
    extra = 0
    fields = ['date', 'hours', 'description']


class ClientTaskInline(admin.TabularInline):
    model = ClientTask
    extra = 0
    fields = ['title', 'status', 'priority', 'due_date', 'estimated_hours']
    show_change_link = True


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'phone', 'source', 'task_count', 'is_active', 'created_at']
    list_filter = ['is_active', 'source']
    search_fields = ['name', 'email', 'company']
    list_editable = ['is_active']
    inlines = [ClientTaskInline]

    def task_count(self, obj):
        return obj.tasks.count()
    task_count.short_description = 'Задач'


@admin.register(ClientTask)
class ClientTaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'client', 'status', 'priority', 'due_date', 'total_hours']
    list_filter = ['status', 'priority', 'client']
    search_fields = ['title', 'client__name']
    list_editable = ['status', 'priority']
    inlines = [WorkLogInline]

    def total_hours(self, obj):
        total = obj.logs.aggregate(total=Sum('hours'))['total']
        return f'{total or 0}ч'
    total_hours.short_description = 'Часов'


@admin.register(WorkLog)
class WorkLogAdmin(admin.ModelAdmin):
    list_display = ['date', 'task', 'hours', 'description']
    list_filter = ['date', 'task__client']
    search_fields = ['task__title', 'description']
    date_hierarchy = 'date'


@admin.register(LearningNote)
class LearningNoteAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'tags', 'is_important', 'created_at']
    list_filter = ['category', 'is_important']
    search_fields = ['title', 'content', 'tags']
    list_editable = ['is_important']
