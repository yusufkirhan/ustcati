from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    
    # Projeler
    path('projeler/', views.projeler, name='projeler'),
    path('projeler/ekle/', views.proje_ekle, name='proje_ekle'),
    path('projeler/duzenle/<int:id>/', views.proje_duzenle, name='proje_duzenle'),
    path('projeler/sil/<int:id>/', views.proje_sil, name='proje_sil'),
    
    # Hizmetler
    path('hizmetler/', views.hizmetler, name='hizmetler'),
    
    # Müşteriler
    path('musteriler/', views.musteriler, name='musteriler'),
    
    # Randevular
    path('randevular/', views.randevular, name='randevular'),
    
    # Hero Section
    path('hero-section/', views.hero_section_list, name='hero_section_list'),
    path('hero-section/ekle/', views.hero_section_create, name='hero_section_create'),
    path('hero-section/<int:pk>/duzenle/', views.hero_section_edit, name='hero_section_edit'),
    path('hero-section/<int:pk>/sil/', views.hero_section_delete, name='hero_section_delete'),
    
    # Medya
    path('medya/', views.medya_listesi, name='medya_listesi'),
    path('medya/yukle/', views.medya_yukle, name='medya_yukle'),
    path('medya/<int:pk>/sil/', views.medya_sil, name='medya_sil'),
    
    # Teklifler
    path('teklifler/', views.teklifler, name='teklifler'),
    path('teklif/<int:teklif_id>/', views.teklif_detay, name='teklif_detay'),
    path('teklif/<int:teklif_id>/okundu/', views.teklif_okundu, name='teklif_okundu'),
    path('teklif/<int:teklif_id>/sil/', views.teklif_sil, name='teklif_sil'),
    path('teklifler/toplu-okundu/', views.toplu_okundu, name='toplu_okundu'),
    path('teklifler/toplu-sil/', views.toplu_sil, name='toplu_sil'),
    
    # Raporlar
    path('raporlar/', views.raporlar, name='raporlar'),
    
    # Ayarlar
    path('ayarlar/', views.ayarlar, name='ayarlar'),
    path('profil/guncelle/', views.profil_guncelle, name='profil_guncelle'),
    path('sifre/degistir/', views.sifre_degistir, name='sifre_degistir'),
    
    # İletişim Mesajları URL'leri
    path('mesajlar/', views.mesajlar, name='mesajlar'),
    path('mesajlar/<int:mesaj_id>/', views.mesaj_detay, name='mesaj_detay'),
    path('mesajlar/<int:mesaj_id>/durum/', views.mesaj_durum_guncelle, name='mesaj_durum_guncelle'),
    path('mesajlar/<int:mesaj_id>/sil/', views.mesaj_sil, name='mesaj_sil'),
    
    path('update-image/', views.update_image, name='update_image'),
    
    # Blog URLs
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/ekle/', views.blog_ekle, name='blog_ekle'),
    path('blog/<int:id>/duzenle/', views.blog_duzenle, name='blog_duzenle'),
    path('blog/<int:id>/sil/', views.blog_sil, name='blog_sil'),
] 