from django.urls import path
from . import views
from . import views as core_views
app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    # path('blog/<slug:slug>/', core_views.blog_detail, name='blog_detail'),
     path('', core_views.home, name='home'),
    path('portfolio/<int:id>/', views.portfolio_detail, name='portfolio_detail'),
    path('careers/', views.careers_list, name='careers'),
    path('careers/<slug:slug>/', views.career_detail, name='career_detail'),
    path('careers/<slug:slug>/apply/', views.apply_job, name='apply_job'),
    path('team/', views.team_members, name='team'),
]