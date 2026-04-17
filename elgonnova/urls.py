from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),

    # path('', core_views.home, name='home'),
    # path('blog/<slug:slug>/', core_views.blog_detail, name='blog_detail'),
    # path('portfolio/<int:id>/', core_views.portfolio_detail, name='portfolio_detail'),
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
