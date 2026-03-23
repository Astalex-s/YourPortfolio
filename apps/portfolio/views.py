from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Project, TechTag


class ProjectListView(ListView):
    model = Project
    template_name = 'portfolio/project_list.html'
    context_object_name = 'projects'
    paginate_by = 9

    def get_queryset(self):
        qs = Project.objects.filter(is_published=True).prefetch_related('tech_stack')
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            qs = qs.filter(tech_stack__name__icontains=tag_slug)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['all_tags'] = TechTag.objects.filter(projects__is_published=True).distinct()
        ctx['active_tag'] = self.request.GET.get('tag', '')
        return ctx


class ProjectDetailView(DetailView):
    model = Project
    template_name = 'portfolio/project_detail.html'
    context_object_name = 'project'

    def get_queryset(self):
        return Project.objects.filter(is_published=True).prefetch_related(
            'screenshots', 'tech_stack'
        )

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        project = self.object
        ctx['related_projects'] = Project.objects.filter(
            is_published=True,
            tech_stack__in=project.tech_stack.all()
        ).exclude(pk=project.pk).distinct()[:3]
        return ctx
