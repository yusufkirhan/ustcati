
from django.db import models
from django.utils.text import slugify
from django.utils import timezone

# Create your models here.

class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name='Başlık')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='İçerik')
    image = models.ImageField(upload_to='blog/', verbose_name='Resim')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Oluşturulma Tarihi')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Güncellenme Tarihi')
    is_active = models.BooleanField(default=True, verbose_name='Aktif')

    class Meta:
        verbose_name = 'Blog Yazısı'
        verbose_name_plural = 'Blog Yazıları'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

class Project(models.Model):
    CATEGORY_CHOICES = [
        ('konut', 'Konut'),
        ('ticari', 'Ticari'),
        ('endustriyel', 'Endüstriyel'),
        ('tumu', 'Tümü')
    ]
    
    title = models.CharField(max_length=200, verbose_name="Proje Başlığı")
    description = models.TextField(verbose_name="Proje Açıklaması")
    image = models.ImageField(upload_to='projects/', verbose_name="Proje Görseli")
    completion_date = models.DateField(verbose_name="Tamamlanma Tarihi", default=timezone.now)
    location = models.CharField(max_length=200, verbose_name="Proje Konumu")
    client = models.CharField(max_length=200, verbose_name="Müşteri")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='tumu', verbose_name="Kategori")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Proje"
        verbose_name_plural = "Projeler"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Service(models.Model):
    STATUS_CHOICES = [
        ('active', 'Aktif'),
        ('inactive', 'Pasif')
    ]
    
    title = models.CharField(max_length=200, verbose_name="Hizmet Adı")
    description = models.TextField(verbose_name="Hizmet Açıklaması")
    icon = models.CharField(max_length=50, verbose_name="İkon")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hizmet"
        verbose_name_plural = "Hizmetler"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Müşteri Adı")
    email = models.EmailField(verbose_name="E-posta")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    company = models.CharField(max_length=200, blank=True, verbose_name="Firma")
    address = models.TextField(blank=True, verbose_name="Adres")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Müşteri"
        verbose_name_plural = "Müşteriler"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Offer(models.Model):
    title = models.CharField(max_length=200, verbose_name="Teklif Başlığı")
    description = models.TextField(verbose_name="Teklif Açıklaması")
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Müşteri")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tutar")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Teklif"
        verbose_name_plural = "Teklifler"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.customer.name}"

class SiteAyarlari(models.Model):
    site_logo = models.ImageField(upload_to='site/', null=True, blank=True)
    footer_logo = models.ImageField(upload_to='site/', null=True, blank=True)
    
    menu_anasayfa = models.CharField(max_length=50, default='Ana Sayfa')
    menu_cati = models.CharField(max_length=50, default='Çatı Sistemleri')
    menu_projeler = models.CharField(max_length=50, default='Projeler')
    menu_referanslar = models.CharField(max_length=50, default='Referanslar')
    menu_iletisim = models.CharField(max_length=50, default='İletişim')
    menu_hizmetler = models.CharField(max_length=50, default='Hizmetler')
    
    footer_telefon = models.CharField(max_length=20)
    footer_email = models.EmailField()
    footer_adres = models.TextField()
    footer_copyright = models.CharField(max_length=200)
    
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return "Site Ayarları"
