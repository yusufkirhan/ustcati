from django.db import models
from django.utils import timezone
import os

class TeklifTalebi(models.Model):
    ad_soyad = models.CharField(max_length=100, verbose_name="Ad Soyad")
    email = models.EmailField(verbose_name="E-posta")
    telefon = models.CharField(max_length=20, verbose_name="Telefon")
    konu = models.CharField(max_length=200, verbose_name="Konu")
    mesaj = models.TextField(verbose_name="Mesaj")
    okundu = models.BooleanField(default=False, verbose_name="Okundu")
    tarih = models.DateTimeField(default=timezone.now, verbose_name="Tarih")

    class Meta:
        verbose_name = "Teklif Talebi"
        verbose_name_plural = "Teklif Talepleri"
        ordering = ['-tarih']

    def __str__(self):
        return f"{self.ad_soyad} - {self.konu}"

class HeroSection(models.Model):
    welcome_text = models.CharField(max_length=100, verbose_name="Karşılama Metni", default="Hoş Geldiniz")
    title = models.CharField(max_length=200, verbose_name="Ana Başlık", default="Profesyonel Çatı")
    rotating_words = models.TextField(verbose_name="Dönen Kelimeler", help_text="Her kelimeyi yeni bir satıra yazın")
    description = models.TextField(verbose_name="Açıklama")
    background_image = models.ImageField(upload_to='hero/', verbose_name="Arka Plan Görseli", null=True, blank=True)
    button_text = models.CharField(max_length=50, verbose_name="Buton Metni", default="Teklif Al")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    order = models.IntegerField(default=0, verbose_name="Sıralama")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    def get_rotating_words_list(self):
        return [word.strip() for word in self.rotating_words.split('\n') if word.strip()]

    class Meta:
        verbose_name = "Ana Sayfa Hero"
        verbose_name_plural = "Ana Sayfa Hero"
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"Hero Section - {self.title}"

class Medya(models.Model):
    baslik = models.CharField(max_length=200)
    resim = models.ImageField(upload_to='medya/')
    yukleme_tarihi = models.DateTimeField(default=timezone.now)

    def delete(self, *args, **kwargs):
        # Önce dosyayı fiziksel olarak sil
        if self.resim:
            if os.path.isfile(self.resim.path):
                os.remove(self.resim.path)
        # Sonra veritabanı kaydını sil
        super().delete(*args, **kwargs)

    class Meta:
        verbose_name = 'Medya'
        verbose_name_plural = 'Medya'
        ordering = ['-yukleme_tarihi']

    def __str__(self):
        return self.baslik

class Contact(models.Model):
    name = models.CharField(max_length=100, verbose_name='Ad Soyad')
    email = models.EmailField(verbose_name='E-posta')
    phone = models.CharField(max_length=20, verbose_name='Telefon')
    subject = models.CharField(max_length=200, verbose_name='Konu')
    message = models.TextField(verbose_name='Mesaj')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Gönderilme Tarihi')
    is_read = models.BooleanField(default=False, verbose_name='Okundu')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Beklemede'),
        ('processed', 'İşlendi'),
        ('answered', 'Yanıtlandı')
    ], default='pending', verbose_name='Durum')

    class Meta:
        verbose_name = 'İletişim Mesajı'
        verbose_name_plural = 'İletişim Mesajları'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.subject}"

class SiteAyarlari(models.Model):
    # Logo ve Menü
    site_logo = models.ImageField(upload_to='site/', verbose_name='Site Logo')
    menu_anasayfa = models.CharField(max_length=50, default='Ana Sayfa', verbose_name='Ana Sayfa Menü')
    menu_cati = models.CharField(max_length=50, default='Çatı Sistemleri', verbose_name='Çatı Sistemleri Menü')
    menu_izolasyon = models.CharField(max_length=50, default='İzolasyon', verbose_name='İzolasyon Menü')
    menu_bakim = models.CharField(max_length=50, default='Bakım & Onarım', verbose_name='Bakım & Onarım Menü')
    menu_projeler = models.CharField(max_length=50, default='Projeler', verbose_name='Projeler Menü')
    menu_referanslar = models.CharField(max_length=50, default='Referanslar', verbose_name='Referanslar Menü')
    menu_iletisim = models.CharField(max_length=50, default='İletişim', verbose_name='İletişim Menü')
    
    # Footer Bilgileri
    footer_logo = models.ImageField(upload_to='site/', verbose_name='Footer Logo')
    footer_telefon = models.CharField(max_length=20, verbose_name="Telefon", null=True, blank=True)
    footer_telefon_aktif = models.BooleanField(default=True, verbose_name="Telefon Aktif")
    footer_email = models.EmailField(blank=True, null=True, verbose_name='E-posta')
    footer_email_aktif = models.BooleanField(default=True, verbose_name="E-posta Aktif")
    footer_adres = models.TextField(blank=True, null=True, verbose_name='Adres')
    footer_adres_aktif = models.BooleanField(default=True, verbose_name="Adres Aktif")
    footer_copyright = models.CharField(max_length=200, verbose_name='Copyright Metni')
    footer_description = models.TextField(verbose_name="Footer Açıklama", null=True, blank=True)
    
    # İletişim Bilgileri
    mobile_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Cep Telefonu')
    mobile_phone_aktif = models.BooleanField(default=True, verbose_name="Cep Telefonu Aktif")
    whatsapp = models.CharField(max_length=20, blank=True, null=True, verbose_name='WhatsApp')
    whatsapp_aktif = models.BooleanField(default=True, verbose_name="WhatsApp Aktif")
    google_maps_url = models.URLField(max_length=255, blank=True, null=True, verbose_name='Google Haritalar Linki')
    google_maps_url_aktif = models.BooleanField(default=True, verbose_name="Google Haritalar Aktif")
    
    # Sosyal Medya
    facebook = models.URLField(max_length=255, blank=True, null=True)
    facebook_aktif = models.BooleanField(default=True, verbose_name="Facebook Aktif")
    twitter = models.URLField(max_length=255, blank=True, null=True)
    twitter_aktif = models.BooleanField(default=True, verbose_name="Twitter Aktif")
    instagram = models.URLField(max_length=255, blank=True, null=True)
    instagram_aktif = models.BooleanField(default=True, verbose_name="Instagram Aktif")
    linkedin = models.URLField(max_length=255, blank=True, null=True)
    linkedin_aktif = models.BooleanField(default=True, verbose_name="LinkedIn Aktif")
    youtube = models.URLField(max_length=255, blank=True, null=True)
    youtube_aktif = models.BooleanField(default=True, verbose_name="YouTube Aktif")

    # Ana Sayfa İçeriği
    feature_title_1 = models.CharField(max_length=100, default='Çatı Onarımı', verbose_name='Özellik Başlık 1')
    feature_desc_1 = models.TextField(default='Her türlü çatı onarım ve bakım hizmetleri', verbose_name='Özellik Açıklama 1')
    feature_link_1 = models.URLField(default='#', verbose_name='Özellik Link 1')
    
    feature_title_2 = models.CharField(max_length=100, default='Çatı İzolasyonu', verbose_name='Özellik Başlık 2')
    feature_desc_2 = models.TextField(default='Su ve ısı yalıtımı çözümleri', verbose_name='Özellik Açıklama 2')
    feature_link_2 = models.URLField(default='#', verbose_name='Özellik Link 2')
    
    feature_title_3 = models.CharField(max_length=100, default='Çatı Sistemleri', verbose_name='Özellik Başlık 3')
    feature_desc_3 = models.TextField(default='Modern çatı sistemleri kurulumu', verbose_name='Özellik Açıklama 3')
    feature_link_3 = models.URLField(default='#', verbose_name='Özellik Link 3')
    
    feature_title_4 = models.CharField(max_length=100, default='Bakım Hizmeti', verbose_name='Özellik Başlık 4')
    feature_desc_4 = models.TextField(default='Periyodik bakım ve kontrol', verbose_name='Özellik Açıklama 4')
    feature_link_4 = models.URLField(default='#', verbose_name='Özellik Link 4')
    
    content_title = models.CharField(max_length=200, default='Profesyonel Çatı Çözümleri', verbose_name='İçerik Başlık')
    content_description = models.TextField(default='Uzman ekibimiz ve kaliteli malzemelerimizle çatı sistemleriniz için en iyi çözümleri sunuyoruz.', verbose_name='İçerik Açıklama')
    
    # Özellik Detayları
    detail_text_1 = models.CharField(max_length=200, default='Profesyonel ekip ve ekipman', verbose_name='Detay Metin 1')
    detail_text_2 = models.CharField(max_length=200, default='Kaliteli malzeme', verbose_name='Detay Metin 2')
    detail_text_3 = models.CharField(max_length=200, default='Uzun ömürlü çözümler', verbose_name='Detay Metin 3')
    
    # Why Choose Us Section
    why_choose_subtitle = models.CharField(max_length=100, default='NEDEN BİZ?', verbose_name='Neden Biz Alt Başlık')
    why_choose_title = models.CharField(max_length=200, default='Kaliteli Hizmet, Uygun Fiyat', verbose_name='Neden Biz Başlık')
    why_choose_description = models.TextField(default='Profesyonel ekibimiz ve kaliteli malzemelerimizle çatı sistemleriniz için en iyi çözümleri sunuyoruz.', verbose_name='Neden Biz Açıklama')
    why_choose_link = models.URLField(default='#', verbose_name='Neden Biz Link')
    
    # Services Section
    services_subtitle = models.CharField(max_length=100, default='HİZMETLERİMİZ', verbose_name='Hizmetler Alt Başlık')
    services_title = models.CharField(max_length=200, default='Size Özel Çözümler', verbose_name='Hizmetler Başlık')
    services_description = models.TextField(default='Modern çatı sistemleri, izolasyon çözümleri ve bakım hizmetleri ile yapılarınızı koruyoruz.', verbose_name='Hizmetler Açıklama')
    services_background = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Hizmetler Arka Plan')
    services_background_position = models.CharField(max_length=50, default='center center', verbose_name='Hizmetler Arka Plan Konumu')

    # Ana Sayfa Resimleri
    feature_image_1 = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Özellik Resim 1')
    feature_image_2 = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Özellik Resim 2')
    feature_image_3 = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Özellik Resim 3')
    feature_image_4 = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Özellik Resim 4')
    content_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='İçerik Resmi')
    why_choose_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Neden Biz Resmi')

    # Modern Roof Section
    modern_roof_title = models.CharField(max_length=200, default='Modern Çatı Sistemleri', verbose_name='Modern Çatı Başlık')
    modern_roof_description = models.TextField(default='Yenilikçi teknolojiler ve uzman ekibimizle çatınızı geleceğe hazırlıyoruz.', verbose_name='Modern Çatı Açıklama')
    modern_roof_link = models.URLField(default='#', verbose_name='Modern Çatı Link')
    modern_roof_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Modern Çatı Resim')

    # Image Cards Section
    # İkinci Kart
    card2_title = models.CharField(max_length=200, default='Çatı İzolasyonu', verbose_name='İkinci Kart Başlık')
    card2_description = models.TextField(default='Profesyonel izolasyon çözümleri', verbose_name='İkinci Kart Açıklama')
    card2_link = models.URLField(default='#', verbose_name='İkinci Kart Link')
    card2_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='İkinci Kart Resim')
    
    # Üçüncü Kart
    card3_title = models.CharField(max_length=200, default='Çatı Bakımı', verbose_name='Üçüncü Kart Başlık')
    card3_description = models.TextField(default='Düzenli bakım ve onarım hizmetleri', verbose_name='Üçüncü Kart Açıklama')
    card3_link = models.URLField(default='#', verbose_name='Üçüncü Kart Link')
    card3_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Üçüncü Kart Resim')

    # Project Section
    project_subtitle = models.CharField(max_length=100, default='PROJELER', verbose_name='Proje Alt Başlık')
    project_title = models.CharField(max_length=200, default='Tamamlanan Projelerimiz', verbose_name='Proje Başlık')
    project_description = models.TextField(default='Başarıyla tamamladığımız projelerimizden örnekleri inceleyin. Modern tasarımlar ve profesyonel uygulamalar ile fark yaratıyoruz.', verbose_name='Proje Açıklama')
    project_background = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Proje Arka Plan Resmi')
    project_background_position = models.CharField(max_length=50, default='center center', verbose_name='Proje Arka Plan Konumu', help_text='Örnek: center center, top center, bottom center, center left, center right')

    # Blog Section
    blog_section_title = models.CharField(max_length=200, default='Son Haberler', verbose_name='Blog Bölüm Başlık')
    blog_section_description = models.TextField(default='En son haberler, güncellemeler ve blog yazılarımız', verbose_name='Blog Bölüm Açıklama')
    
    # Blog Post 1
    blog_post1_title = models.CharField(max_length=200, default='Blog Post 1 Başlık', verbose_name='Blog Post 1 Başlık')
    blog_post1_description = models.TextField(default='Blog post 1 açıklaması burada yer alacak.', verbose_name='Blog Post 1 Açıklama')
    blog_post1_link = models.URLField(default='#', verbose_name='Blog Post 1 Link')
    blog_post1_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Blog Post 1 Resim')
    
    # Blog Post 2
    blog_post2_title = models.CharField(max_length=200, default='Blog Post 2 Başlık', verbose_name='Blog Post 2 Başlık')
    blog_post2_description = models.TextField(default='Blog post 2 açıklaması burada yer alacak.', verbose_name='Blog Post 2 Açıklama')
    blog_post2_link = models.URLField(default='#', verbose_name='Blog Post 2 Link')
    blog_post2_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Blog Post 2 Resim')
    
    # Blog Post 3
    blog_post3_title = models.CharField(max_length=200, default='Blog Post 3 Başlık', verbose_name='Blog Post 3 Başlık')
    blog_post3_description = models.TextField(default='Blog post 3 açıklaması burada yer alacak.', verbose_name='Blog Post 3 Açıklama')
    blog_post3_link = models.URLField(default='#', verbose_name='Blog Post 3 Link')
    blog_post3_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Blog Post 3 Resim')

    # Contact Section
    contact_title = models.CharField(max_length=200, default='İletişime Geçin', verbose_name='İletişim Başlık')
    contact_description = models.TextField(default='Bizimle iletişime geçmek için aşağıdaki formu doldurun.', verbose_name='İletişim Açıklama')
    contact_address = models.TextField(default='2601 Beaumont Ave Liberty, Texas', verbose_name='İletişim Adres')
    contact_phone = models.CharField(max_length=20, default='+1-(903) 482-5172', verbose_name='İletişim Telefon')
    contact_email = models.EmailField(default='info@ustcati.com', verbose_name='İletişim E-posta')

    # Çatı Sistemleri Sayfası
    # Hero Section
    roof_systems_title = models.CharField(max_length=200, default='Modern Çatı Sistemleri', verbose_name='Çatı Sistemleri Başlık')
    roof_systems_subtitle = models.TextField(default='Yenilikçi teknolojiler ve uzman ekibimizle çatınızı geleceğe hazırlıyoruz', verbose_name='Çatı Sistemleri Alt Başlık')
    roof_systems_hero_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Çatı Sistemleri Hero Resim')
    
    # Çözümler Section
    roof_systems_solutions_title = models.CharField(max_length=200, default='Çatı Sistemleri Çözümlerimiz', verbose_name='Çatı Sistemleri Çözümler Başlık')
    
    # Çatı Tipi 1 (Kiremit)
    roof_type1_title = models.CharField(max_length=200, default='Kiremit Çatı Sistemleri', verbose_name='Kiremit Çatı Başlık')
    roof_type1_description = models.TextField(default='Geleneksel ve modern kiremit çatı sistemleri ile binanızın estetiğini ve dayanıklılığını artırın.', verbose_name='Kiremit Çatı Açıklama')
    roof_type1_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Kiremit Çatı Resim')
    roof_type1_feature1 = models.CharField(max_length=200, default='Uzun Ömürlü Dayanıklılık', verbose_name='Kiremit Çatı Özellik 1')
    roof_type1_feature2 = models.CharField(max_length=200, default='Estetik Görünüm', verbose_name='Kiremit Çatı Özellik 2')
    roof_type1_feature3 = models.CharField(max_length=200, default='Doğal Havalandırma', verbose_name='Kiremit Çatı Özellik 3')
    
    # Çatı Tipi 2 (Metal)
    roof_type2_title = models.CharField(max_length=200, default='Metal Çatı Sistemleri', verbose_name='Metal Çatı Başlık')
    roof_type2_description = models.TextField(default='Hafif, dayanıklı ve modern metal çatı sistemleri ile yapınızı güvence altına alın.', verbose_name='Metal Çatı Açıklama')
    roof_type2_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Metal Çatı Resim')
    roof_type2_feature1 = models.CharField(max_length=200, default='Hafif Yapı', verbose_name='Metal Çatı Özellik 1')
    roof_type2_feature2 = models.CharField(max_length=200, default='Hızlı Montaj', verbose_name='Metal Çatı Özellik 2')
    roof_type2_feature3 = models.CharField(max_length=200, default='Minimum Bakım', verbose_name='Metal Çatı Özellik 3')
    
    # Çatı Tipi 3 (Shingle)
    roof_type3_title = models.CharField(max_length=200, default='Shingle Çatı Sistemleri', verbose_name='Shingle Çatı Başlık')
    roof_type3_description = models.TextField(default='Modern ve estetik shingle çatı sistemleri ile yapınıza değer katın.', verbose_name='Shingle Çatı Açıklama')
    roof_type3_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Shingle Çatı Resim')
    roof_type3_feature1 = models.CharField(max_length=200, default='Çeşitli Renk Seçenekleri', verbose_name='Shingle Çatı Özellik 1')
    roof_type3_feature2 = models.CharField(max_length=200, default='Kolay Uygulama', verbose_name='Shingle Çatı Özellik 2')
    roof_type3_feature3 = models.CharField(max_length=200, default='Ekonomik Çözüm', verbose_name='Shingle Çatı Özellik 3')
    
    # Özellikler Section
    features_title = models.CharField(max_length=200, default='Neden Çatı Sistemlerimizi Tercih Etmelisiniz?', verbose_name='Özellikler Başlık')
    features_image = models.ImageField(upload_to='medya/', null=True, blank=True, verbose_name='Özellikler Resim')
    
    # Özellik 1
    feature1_title = models.CharField(max_length=200, default='Maksimum Koruma', verbose_name='Özellik 1 Başlık')
    feature1_description = models.TextField(default='En zorlu hava koşullarına karşı tam koruma sağlayan çatı sistemleri.', verbose_name='Özellik 1 Açıklama')
    
    # Özellik 2
    feature2_title = models.CharField(max_length=200, default='Enerji Verimliliği', verbose_name='Özellik 2 Başlık')
    feature2_description = models.TextField(default='Isı yalıtımı ile enerji tasarrufu sağlayan akıllı çözümler.', verbose_name='Özellik 2 Açıklama')
    
    # Özellik 3
    feature3_title = models.CharField(max_length=200, default='Profesyonel Montaj', verbose_name='Özellik 3 Başlık')
    feature3_description = models.TextField(default='Uzman ekibimiz ile hatasız ve hızlı montaj hizmeti.', verbose_name='Özellik 3 Açıklama')
    
    # Süreç Section
    process_title = models.CharField(max_length=200, default='Çatı Sistemi Kurulum Süreci', verbose_name='Süreç Başlık')
    
    # Süreç Adım 1
    process_step1_title = models.CharField(max_length=200, default='Keşif', verbose_name='Süreç Adım 1 Başlık')
    process_step1_description = models.TextField(default='Ücretsiz keşif hizmeti ile ihtiyaçlarınızı belirleyelim.', verbose_name='Süreç Adım 1 Açıklama')
    
    # Süreç Adım 2
    process_step2_title = models.CharField(max_length=200, default='Planlama', verbose_name='Süreç Adım 2 Başlık')
    process_step2_description = models.TextField(default='Size özel çatı sistemi planlaması yapalım.', verbose_name='Süreç Adım 2 Açıklama')
    
    # Süreç Adım 3
    process_step3_title = models.CharField(max_length=200, default='Uygulama', verbose_name='Süreç Adım 3 Başlık')
    process_step3_description = models.TextField(default='Profesyonel ekibimiz ile montajı gerçekleştirelim.', verbose_name='Süreç Adım 3 Açıklama')
    
    # Süreç Adım 4
    process_step4_title = models.CharField(max_length=200, default='Kontrol', verbose_name='Süreç Adım 4 Başlık')
    process_step4_description = models.TextField(default='Son kontroller ile kalite güvencesi sağlayalım.', verbose_name='Süreç Adım 4 Açıklama')
    
    # CTA Section
    cta_title = models.CharField(max_length=200, default='Çatınız İçin Profesyonel Çözümler', verbose_name='CTA Başlık')
    cta_description = models.TextField(default='Ücretsiz keşif ve fiyat teklifi için hemen bizimle iletişime geçin.', verbose_name='CTA Açıklama')

    # İletişim Sayfası
    contact_hero_title = models.CharField(max_length=200, blank=True, null=True)
    contact_hero_subtitle = models.CharField(max_length=500, blank=True, null=True)
    contact_hero_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    # İletişim Bilgileri
    contact_address = models.TextField(blank=True, null=True)
    contact_phone = models.TextField(blank=True, null=True)
    contact_email = models.TextField(blank=True, null=True)
    
    # Form Bölümü
    contact_form_title = models.CharField(max_length=200, blank=True, null=True)
    contact_form_description = models.TextField(blank=True, null=True)
    
    # Çalışma Saatleri
    working_hours_title = models.CharField(max_length=200, blank=True, null=True)
    working_hours_weekday = models.CharField(max_length=200, blank=True, null=True)
    working_hours_saturday = models.CharField(max_length=200, blank=True, null=True)
    working_hours_sunday = models.CharField(max_length=200, blank=True, null=True)
    
    # Sosyal Medya
    social_media_title = models.CharField(max_length=200, blank=True, null=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    instagram_link = models.URLField(blank=True, null=True)
    linkedin_link = models.URLField(blank=True, null=True)
    
    # Harita
    map_embed_url = models.TextField(blank=True, null=True)

    # Projeler Sayfası
    projects_hero_title = models.CharField(max_length=200, blank=True, null=True)
    projects_hero_subtitle = models.CharField(max_length=200, blank=True, null=True)
    projects_hero_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    # Proje Kartları
    project1_title = models.CharField(max_length=200, blank=True, null=True)
    project1_description = models.TextField(blank=True, null=True)
    project1_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    project1_category = models.CharField(max_length=50, blank=True, null=True)
    project1_details = models.TextField(blank=True, null=True)
    project1_location = models.CharField(max_length=200, blank=True, null=True)
    project1_area = models.CharField(max_length=50, blank=True, null=True)
    project1_duration = models.CharField(max_length=50, blank=True, null=True)
    project1_material = models.CharField(max_length=100, blank=True, null=True)
    project1_insulation = models.CharField(max_length=100, blank=True, null=True)
    project1_warranty = models.CharField(max_length=50, blank=True, null=True)
    
    project2_title = models.CharField(max_length=200, blank=True, null=True)
    project2_description = models.TextField(blank=True, null=True)
    project2_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    project2_category = models.CharField(max_length=50, blank=True, null=True)
    project2_details = models.TextField(blank=True, null=True)
    project2_location = models.CharField(max_length=200, blank=True, null=True)
    project2_area = models.CharField(max_length=50, blank=True, null=True)
    project2_duration = models.CharField(max_length=50, blank=True, null=True)
    project2_material = models.CharField(max_length=100, blank=True, null=True)
    project2_insulation = models.CharField(max_length=100, blank=True, null=True)
    project2_warranty = models.CharField(max_length=50, blank=True, null=True)
    
    project3_title = models.CharField(max_length=200, blank=True, null=True)
    project3_description = models.TextField(blank=True, null=True)
    project3_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    project3_category = models.CharField(max_length=50, blank=True, null=True)
    project3_details = models.TextField(blank=True, null=True)
    project3_location = models.CharField(max_length=200, blank=True, null=True)
    project3_area = models.CharField(max_length=50, blank=True, null=True)
    project3_duration = models.CharField(max_length=50, blank=True, null=True)
    project3_material = models.CharField(max_length=100, blank=True, null=True)
    project3_insulation = models.CharField(max_length=100, blank=True, null=True)
    project3_warranty = models.CharField(max_length=50, blank=True, null=True)
    
    # Proje İstatistikleri
    projects_completed = models.CharField(max_length=50, blank=True, null=True)
    projects_active = models.CharField(max_length=50, blank=True, null=True)
    projects_experience = models.CharField(max_length=50, blank=True, null=True)
    projects_customers = models.CharField(max_length=50, blank=True, null=True)

    # Referanslar Sayfası
    references_hero_title = models.CharField(max_length=200, blank=True, null=True)
    references_hero_subtitle = models.CharField(max_length=500, blank=True, null=True)
    references_hero_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    # Markalar
    brand1_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    brand2_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    brand3_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    brand4_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    # Müşteri Yorumları
    testimonial1_content = models.TextField(blank=True, null=True)
    testimonial1_name = models.CharField(max_length=100, blank=True, null=True)
    testimonial1_project = models.CharField(max_length=100, blank=True, null=True)
    testimonial1_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    testimonial2_content = models.TextField(blank=True, null=True)
    testimonial2_name = models.CharField(max_length=100, blank=True, null=True)
    testimonial2_project = models.CharField(max_length=100, blank=True, null=True)
    testimonial2_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    testimonial3_content = models.TextField(blank=True, null=True)
    testimonial3_name = models.CharField(max_length=100, blank=True, null=True)
    testimonial3_project = models.CharField(max_length=100, blank=True, null=True)
    testimonial3_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    
    # Sertifikalar
    certificate1_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    certificate1_title = models.CharField(max_length=100, blank=True, null=True)
    certificate1_description = models.TextField(blank=True, null=True)
    
    certificate2_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    certificate2_title = models.CharField(max_length=100, blank=True, null=True)
    certificate2_description = models.TextField(blank=True, null=True)
    
    certificate3_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    certificate3_title = models.CharField(max_length=100, blank=True, null=True)
    certificate3_description = models.TextField(blank=True, null=True)
    
    certificate4_image = models.ImageField(upload_to='medya/', blank=True, null=True)
    certificate4_title = models.CharField(max_length=100, blank=True, null=True)
    certificate4_description = models.TextField(blank=True, null=True)
    
    # CTA Bölümü
    references_cta_title = models.CharField(max_length=200, blank=True, null=True)
    references_cta_description = models.TextField(blank=True, null=True)

    # Hizmetler Sayfası
    services_hero_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmetler Hero Başlık')
    services_hero_subtitle = models.CharField(max_length=500, blank=True, null=True, verbose_name='Hizmetler Hero Alt Başlık')
    services_hero_image = models.ImageField(upload_to='medya/', blank=True, null=True, verbose_name='Hizmetler Hero Resim')

    # Hizmet Kartları
    service1_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 1 Başlık')
    service1_description = models.TextField(blank=True, null=True, verbose_name='Hizmet 1 Açıklama')
    service1_feature1 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 1 Özellik 1')
    service1_feature2 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 1 Özellik 2')
    service1_feature3 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 1 Özellik 3')

    service2_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 2 Başlık')
    service2_description = models.TextField(blank=True, null=True, verbose_name='Hizmet 2 Açıklama')
    service2_feature1 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 2 Özellik 1')
    service2_feature2 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 2 Özellik 2')
    service2_feature3 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 2 Özellik 3')

    service3_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 3 Başlık')
    service3_description = models.TextField(blank=True, null=True, verbose_name='Hizmet 3 Açıklama')
    service3_feature1 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 3 Özellik 1')
    service3_feature2 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 3 Özellik 2')
    service3_feature3 = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmet 3 Özellik 3')

    # CTA Bölümü
    services_cta_title = models.CharField(max_length=200, blank=True, null=True, verbose_name='Hizmetler CTA Başlık')
    services_cta_description = models.TextField(blank=True, null=True, verbose_name='Hizmetler CTA Açıklama')

    class Meta:
        verbose_name = 'Site Ayarları'
        verbose_name_plural = 'Site Ayarları'

    def __str__(self):
        return 'Site Ayarları'

    def save(self, *args, **kwargs):
        if not self.pk and SiteAyarlari.objects.exists():
            return # Sadece bir kayıt olabilir
        return super(SiteAyarlari, self).save(*args, **kwargs)

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='Kullanıcı')
    profile_image = models.ImageField(upload_to='profiles/', verbose_name='Profil Fotoğrafı', null=True, blank=True)

    class Meta:
        verbose_name = 'Kullanıcı Profili'
        verbose_name_plural = 'Kullanıcı Profilleri'

    def __str__(self):
        return self.user.username

class Project(models.Model):
    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    description = models.TextField(verbose_name="Proje Açıklaması")
    image = models.ImageField(upload_to='projects/', verbose_name="Proje Resmi", null=True, blank=True)
    category = models.CharField(max_length=50, verbose_name="Kategori", choices=[
        ('residential', 'Konut'),
        ('commercial', 'Ticari'),
        ('industrial', 'Endüstriyel')
    ])
    location = models.CharField(max_length=200, verbose_name="Konum")
    area = models.CharField(max_length=50, verbose_name="Alan")
    duration = models.CharField(max_length=50, verbose_name="Süre")
    material = models.CharField(max_length=100, verbose_name="Malzeme")
    insulation = models.CharField(max_length=100, verbose_name="İzolasyon")
    warranty = models.CharField(max_length=50, verbose_name="Garanti")
    details = models.TextField(verbose_name="Proje Detayları", null=True, blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Oluşturulma Tarihi")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Güncellenme Tarihi")

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_at']

    def __str__(self):
        return self.title 