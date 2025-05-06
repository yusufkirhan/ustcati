"""
URL configuration for ustcati project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.static import serve
from django.urls import re_path

urlpatterns = [
    path('', include('core.urls')),
    path('panel/', include('dashboard.urls')),
    
    # Login URL'leri
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='dashboard/login.html',
        redirect_field_name='next'
    ), name='login'),
    
    path('accounts/logout/', auth_views.LogoutView.as_view(
        next_page='login'
    ), name='logout'),

    # Media dosyaları için özel URL
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

# Static dosyaları için
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
