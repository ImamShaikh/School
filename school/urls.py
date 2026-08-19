from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('teachers/', views.teachers_view, name='teachers'),
    path('events/', views.events_view, name='events'),
    path('gallery/', views.gallery_view, name='gallery'),
    path('news/', views.news_view, name='news'),
    path('news/<slug:slug>/', views.news_detail, name='news-detail'),
    path('contact-us/', views.contact_view, name='contact'),
    path('register/', views.register_view, name='register'),
]
