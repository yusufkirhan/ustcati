from django.contrib import admin
from django.contrib.auth.models import User, Group
from .models import TeklifTalebi, HeroSection, Medya, Contact, SiteAyarlari, UserProfile, Project

# Model importlarınızı buraya ekleyin
# from .models import YourModel

# Admin panel özelleştirmeleri
admin.site.site_header = 'Üst Çatı Yönetim Paneli'
admin.site.site_title = 'Üst Çatı Admin'
admin.site.index_title = 'Yönetim Paneli'

# Model kayıtlarınızı buraya ekleyin
@admin.register(TeklifTalebi)
class TeklifTalebiAdmin(admin.ModelAdmin):
    list_display = ('ad_soyad', 'email', 'telefon', 'konu', 'okundu', 'tarih')
    list_filter = ('okundu', 'tarih')
    search_fields = ('ad_soyad', 'email', 'telefon', 'konu', 'mesaj')
    list_per_page = 20
    date_hierarchy = 'tarih'

    def mark_as_read(self, request, queryset):
        queryset.update(okundu=True)
    mark_as_read.short_description = "Seçili talepleri okundu olarak işaretle"

    actions = ['mark_as_read']

@admin.register(HeroSection)
class HeroSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Ana Bilgiler', {
            'fields': ('welcome_text', 'title', 'description', 'background_image')
        }),
        ('Dönen Kelimeler', {
            'fields': ('rotating_words',),
            'description': 'Her kelimeyi yeni bir satıra yazın. Örnek:\nSistemleri\nÇözümleri\nHizmetleri'
        }),
        ('Buton ve Durum', {
            'fields': ('button_text', 'is_active')
        }),
        ('Tarihler', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Medya)
class MedyaAdmin(admin.ModelAdmin):
    list_display = ('baslik', 'yukleme_tarihi')
    search_fields = ('baslik',)
    list_per_page = 20
    date_hierarchy = 'yukleme_tarihi'

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'subject', 'created_at', 'is_read', 'status')
    list_filter = ('is_read', 'status', 'created_at')
    search_fields = ('name', 'email', 'phone', 'subject', 'message')
    readonly_fields = ('created_at',)
    list_per_page = 20
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
    mark_as_read.short_description = "Seçili mesajları okundu olarak işaretle"
    
    actions = ['mark_as_read']

@admin.register(SiteAyarlari)
class SiteAyarlariAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Logo ve Menü', {
            'fields': ('site_logo', 'menu_anasayfa', 'menu_cati', 'menu_izolasyon', 
                      'menu_bakim', 'menu_projeler', 'menu_referanslar', 'menu_iletisim')
        }),
        ('Footer Bilgileri', {
            'fields': ('footer_logo', 'footer_telefon', 'footer_email', 'footer_adres', 'footer_copyright')
        }),
        ('Sosyal Medya', {
            'fields': ('facebook', 'twitter', 'instagram', 'linkedin', 'youtube')
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_image')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'is_active', 'created_at')
    list_filter = ('category', 'is_active')
    search_fields = ('title', 'description', 'location')
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)

# @admin.register(YourModel)
# class YourModelAdmin(admin.ModelAdmin):
#     list_display = ['field1', 'field2']
#     search_fields = ['field1']
#     list_filter = ['field2']