from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('hizmetlerimiz/', views.services, name='services'),
    path('cati-sistemleri/', views.roof_systems, name='roof_systems'),
    path('projeler/', views.projects, name='projects'),
    path('referanslar/', views.references, name='references'),
    path('iletisim/', views.contact, name='contact'),
    path('teklif-al/', views.submit_teklif, name='submit_teklif'),
    path('api/save-content/', views.save_content, name='save_content'),
    path('api/upload-image/', views.upload_image, name='upload_image'),
    path('api/get-media/', views.get_media, name='get_media'),
    path('blog/<int:id>/', views.blog_detail, name='blog_detail'),
] 