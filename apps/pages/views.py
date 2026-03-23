from django.views.generic import TemplateView, FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from apps.portfolio.models import Project
from .models import SiteSettings
from .forms import ContactForm

DEFAULT_SKILLS = [
    {'name': 'Python',     'percent': 90},
    {'name': 'Django',     'percent': 85},
    {'name': 'PostgreSQL', 'percent': 80},
    {'name': 'Docker',     'percent': 75},
    {'name': 'REST API',   'percent': 88},
    {'name': 'Git',        'percent': 85},
]


class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['featured_projects'] = Project.objects.filter(
            is_published=True, is_featured=True
        ).prefetch_related('tech_stack')[:6]
        return ctx


class AboutView(TemplateView):
    template_name = 'pages/about.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['default_skills'] = DEFAULT_SKILLS
        return ctx


class ServicesView(TemplateView):
    template_name = 'pages/services.html'


class ResumeView(TemplateView):
    template_name = 'pages/resume.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        site = SiteSettings.objects.first()
        ctx['cv_data'] = site.cv_data if site else {}
        ctx['certificates'] = site.certificates.all() if site else []
        ctx['educations'] = site.educations.all() if site else []
        ctx['experiences'] = site.experiences.all() if site else []
        return ctx


class ContactView(FormView):
    template_name = 'pages/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('pages:contact')

    def form_valid(self, form):
        contact_msg = form.save()
        try:
            send_mail(
                subject=f'[Portfolio] {contact_msg.subject}',
                message=(
                    f'От: {contact_msg.name} <{contact_msg.email}>\n\n'
                    f'{contact_msg.message}'
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass
        messages.success(self.request, 'Сообщение отправлено! Я свяжусь с вами в ближайшее время.')
        return super().form_valid(form)
