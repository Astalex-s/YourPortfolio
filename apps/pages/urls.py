from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('',          views.HomeView.as_view(),     name='home'),
    path('about/',    views.AboutView.as_view(),    name='about'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('resume/',   views.ResumeView.as_view(),   name='resume'),
    path('contact/',  views.ContactView.as_view(),  name='contact'),
]
