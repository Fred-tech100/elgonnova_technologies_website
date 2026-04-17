from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.dashboard_login_view, name='dashboard_login'),
    path('logout/', views.dashboard_logout_view, name='dashboard_logout'),
    path('', views.dashboard_home, name='dashboard_home'),
    path('posts/', views.dashboard_posts, name='dashboard_posts'),
    path('posts/add/', views.add_post, name='add_post'),
    path('posts/edit/<int:id>/', views.edit_post, name='edit_post'),
    path('posts/delete/<int:id>/', views.delete_post, name='delete_post'),
    path('services/', views.dashboard_services, name='dashboard_services'),
    path('portfolio/', views.dashboard_portfolio, name='dashboard_portfolio'),
    path('testimonials/', views.dashboard_testimonials, name='dashboard_testimonials'),
    path('messages/', views.dashboard_messages, name='dashboard_messages'),
    path('subscribers/', views.dashboard_subscribers, name='dashboard_subscribers'),
    path('settings/', views.dashboard_settings, name='dashboard_settings'),
    # New URLs
    path('team/', views.dashboard_team, name='dashboard_team'),
    path('careers/', views.dashboard_careers, name='dashboard_careers'),
    path('applications/', views.dashboard_applications, name='dashboard_applications'),
    path('ceo-message/', views.dashboard_ceo_message, name='dashboard_ceo_message'),
    path('api/team-member/<int:id>/', views.get_team_member_api, name='api_team_member'),
]