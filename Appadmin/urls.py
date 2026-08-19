from django.urls import path
from . import views

app_name = 'Appadmin'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard, name='dashboard'),
    
    # Teachers CRUD
    path('teachers/', views.teacher_list, name='teacher-list'),
    path('teachers/add/', views.teacher_add, name='teacher-add'),
    path('teachers/<int:id>/edit/', views.teacher_edit, name='teacher-edit'),
    path('teachers/<int:id>/delete/', views.teacher_delete, name='teacher-delete'),
    
    # Events CRUD
    path('events/', views.event_list, name='event-list'),
    path('events/add/', views.event_add, name='event-add'),
    path('events/<int:id>/edit/', views.event_edit, name='event-edit'),
    path('events/<int:id>/delete/', views.event_delete, name='event-delete'),
    
    # News CRUD
    path('news/', views.news_list, name='news-list'),
    path('news/add/', views.news_add, name='news-add'),
    path('news/<int:id>/edit/', views.news_edit, name='news-edit'),
    path('news/<int:id>/delete/', views.news_delete, name='news-delete'),
    
    # Gallery CRUD
    path('gallery/', views.gallery_list, name='gallery-list'),
    path('gallery/add/', views.gallery_add, name='gallery-add'),
    path('gallery/<int:id>/delete/', views.gallery_delete, name='gallery-delete'),
    
    # Registrations Management
    path('registrations/', views.registration_list, name='registration-list'),
    path('registrations/<int:id>/status/<str:status>/', views.registration_status_update, name='registration-status-update'),
    path('registrations/<int:id>/delete/', views.registration_delete, name='registration-delete'),
    
    # Messages Management
    path('messages/', views.message_list, name='message-list'),
    path('messages/<int:id>/toggle-read/', views.message_read_toggle, name='message-read-toggle'),
    path('messages/<int:id>/delete/', views.message_delete, name='message-delete'),
    
    # General School Info Edit
    path('school-info/', views.school_info_edit, name='school-info'),
    
    # User Management (Super Admin only)
    path('users/', views.user_list, name='user-list'),
    path('users/add/', views.user_add, name='user-add'),
    path('users/<int:id>/edit/', views.user_edit, name='user-edit'),
    path('users/<int:id>/delete/', views.user_delete, name='user-delete'),
]
