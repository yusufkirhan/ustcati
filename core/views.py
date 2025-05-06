from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from .models import TeklifTalebi, HeroSection, Contact, SiteAyarlari, Medya
from dashboard.models import Project
from django.contrib import messages
from django.views.decorators.http import require_POST, require_http_methods
import json
from .forms import ContactForm
from dashboard.models import Blog

def get_common_context(request):
    site_ayarlari, _ = SiteAyarlari.objects.get_or_create(pk=1)
    return {
        'site_ayarlari': site_ayarlari
    }

def home(request):
    # Aktif hero section'ları sıralı olarak al
    hero_sections = HeroSection.objects.filter(is_active=True).order_by('order', 'created_at')
    
    site_settings = SiteAyarlari.objects.first()
    if not site_settings:
        site_settings = SiteAyarlari.objects.create()
    
    # Son eklenen 3 aktif blog yazısını al
    blog_posts = Blog.objects.filter(is_active=True).order_by('-created_at')[:3]
        
    context = {
        'hero_sections': hero_sections,
        'site': site_settings,
        'is_admin': request.user.is_authenticated and request.user.is_staff,
        'blog_posts': blog_posts
    }
    return render(request, 'home.html', context)

def services(request):
    # Site ayarlarını al
    site = SiteAyarlari.objects.first()
    if not site:
        site = SiteAyarlari.objects.create()
    
    # Admin kontrolü
    is_admin = request.user.is_authenticated and request.user.is_staff
    
    context = {
        'site': site,
        'is_admin': is_admin
    }
    
    return render(request, 'services.html', context)

def roof_systems(request):
    site_settings = SiteAyarlari.objects.first()
    if not site_settings:
        site_settings = SiteAyarlari.objects.create()
        
    context = {
        'site': site_settings,
        'is_admin': request.user.is_authenticated and request.user.is_staff
    }
    return render(request, 'roof_systems.html', context)

def projects(request):
    site = SiteAyarlari.objects.first()
    if not site:
        site = SiteAyarlari.objects.create()
    
    # Aktif projeleri al
    projects = Project.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'site': site,
        'is_admin': request.user.is_authenticated and request.user.is_staff,
        'projects': projects
    }
    return render(request, 'projects.html', context)

def references(request):
    # Site ayarlarını al
    site = SiteAyarlari.objects.first()
    if not site:
        site = SiteAyarlari.objects.create()
    
    # Admin kontrolü
    is_admin = request.user.is_authenticated and request.user.is_staff
    
    context = {
        'site': site,
        'is_admin': is_admin
    }
    
    return render(request, 'references.html', context)

def contact(request):
    site = SiteAyarlari.objects.first()
    if not site:
        site = SiteAyarlari.objects.create()
    
    if request.method == 'POST':
        try:
            contact = Contact.objects.create(
                name=request.POST.get('name'),
                email=request.POST.get('email'),
                phone=request.POST.get('phone'),
                subject=request.POST.get('subject'),
                message=request.POST.get('message')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Mesajınız başarıyla gönderildi.'
            })
        except Exception as e:
            print("İletişim formu hatası:", str(e))
            return JsonResponse({
                'status': 'error',
                'message': 'Bir hata oluştu. Lütfen tekrar deneyin.'
            }, status=400)
    
    context = {
        'site': site,
        'form': ContactForm(),
        'is_admin': request.user.is_authenticated and request.user.is_staff
    }
    return render(request, 'contact.html', context)

@csrf_exempt
def teklif_al(request):
    if request.method == 'POST':
        try:
            teklif = TeklifTalebi.objects.create(
                ad_soyad=request.POST.get('ad_soyad'),
                email=request.POST.get('email'),
                telefon=request.POST.get('telefon'),
                konu=request.POST.get('konu'),
                mesaj=request.POST.get('mesaj')
            )
            return JsonResponse({
                'status': 'success',
                'message': 'Teklif talebiniz başarıyla alındı.'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Bir hata oluştu. Lütfen tekrar deneyin.'
            })
    return JsonResponse({'status': 'error', 'message': 'Geçersiz istek.'})

@ensure_csrf_cookie
@require_http_methods(["POST"])
def submit_teklif(request):
    try:
        data = json.loads(request.body)
        print("Gelen veri:", data)  # Debug için
        
        teklif = TeklifTalebi.objects.create(
            ad_soyad=data.get('name'),
            email=data.get('email'),
            telefon=data.get('phone'),
            konu=data.get('subject'),
            mesaj=data.get('message')
        )
        print("Teklif oluşturuldu:", teklif)  # Debug için
        
        return JsonResponse({
            'status': 'success',
            'message': 'Mesajınız başarıyla alındı. En kısa sürede size dönüş yapacağız.'
        })
    except json.JSONDecodeError as e:
        print("JSON decode hatası:", str(e))  # Debug için
        return JsonResponse({
            'status': 'error',
            'message': 'Geçersiz veri formatı.'
        }, status=400)
    except Exception as e:
        print("Genel hata:", str(e))  # Debug için
        return JsonResponse({
            'status': 'error',
            'message': 'Bir hata oluştu. Lütfen tekrar deneyin.'
        }, status=500)

@csrf_exempt
def save_content(request):
    try:
        data = json.loads(request.body)
        field = data.get('field')
        content = data.get('content')
        
        print(f"Kaydedilecek alan: {field}, İçerik: {content}")
        
        site_settings = SiteAyarlari.objects.first()
        if not site_settings:
            site_settings = SiteAyarlari.objects.create()
            
        # Alan kontrolü
        if not hasattr(site_settings, field):
            return JsonResponse({
                'status': 'error',
                'message': f'Geçersiz alan: {field}'
            }, status=400)

        # İçeriği kaydet
        setattr(site_settings, field, content)
        site_settings.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'İçerik başarıyla kaydedildi',
            'content': content
        })
            
    except Exception as e:
        print(f"Hata: {str(e)}")
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=500)

@require_POST
@csrf_exempt
def upload_image(request):
    try:
        image = request.FILES.get('image')
        field = request.POST.get('field')
        
        if not image:
            return JsonResponse({'status': 'error', 'message': 'Resim bulunamadı'}, status=400)
            
        # Resim alanı kontrolü
        valid_image_fields = ['feature_image_1', 'feature_image_2', 'feature_image_3', 'feature_image_4', 
                            'content_image', 'why_choose_image', 'site_logo', 'footer_logo',
                            'modern_roof_image', 'card2_image', 'card3_image', 'services_background']  # services_background eklendi
        
        if field not in valid_image_fields:
            return JsonResponse({'status': 'error', 'message': 'Geçersiz resim alanı'}, status=400)
            
        # Medya modeline kaydet
        medya = Medya.objects.create(
            baslik=f"{field} resmi",
            resim=image
        )
        
        # Site ayarlarını güncelle
        site_settings = SiteAyarlari.objects.first()
        if not site_settings:
            site_settings = SiteAyarlari.objects.create()
            
        # Eski resmi sil
        old_image = getattr(site_settings, field, None)
        if old_image:
            try:
                old_image.delete()
            except:
                pass
            
        # Yeni resmi kaydet
        setattr(site_settings, field, medya.resim)
        site_settings.save()
        
        return JsonResponse({
            'status': 'success',
            'image_url': medya.resim.url,
            'image_id': medya.id
        })
    except Exception as e:
        print('Hata:', str(e))  # Hata ayıklama için
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def get_media(request):
    try:
        media_items = Medya.objects.all().order_by('-yukleme_tarihi')
        media_list = [{
            'id': item.id,
            'url': item.resim.url,
            'title': item.baslik
        } for item in media_items]
        
        return JsonResponse({
            'status': 'success',
            'media': media_list
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

def index(request):
    # Aktif hero section'ları sıralı olarak al
    hero_sections = HeroSection.objects.filter(is_active=True).order_by('order')
    
    # Blog yazılarını al
    blog_posts = Blog.objects.filter(is_active=True).order_by('-created_at')[:3]
    
    context = {
        'hero_sections': hero_sections,
        'blog_posts': blog_posts,
    }
    
    return render(request, 'core/index.html', context)

def blog_detail(request, id):
    # Blog yazısını getir
    post = get_object_or_404(Blog, id=id, is_active=True)
    
    # Site ayarlarını al
    site = SiteAyarlari.objects.first()
    if not site:
        site = SiteAyarlari.objects.create()
    
    context = {
        'post': post,
        'site': site,
        'is_admin': request.user.is_authenticated and request.user.is_staff
    }
    return render(request, 'core/blog_detail.html', context)

def cati_sistemleri(request):
    context = get_common_context()
    # ... diğer context verileri ...
    return render(request, 'cati-sistemleri.html', context)

def projeler(request):
    context = get_common_context()
    # ... diğer context verileri ...
    return render(request, 'projeler.html', context)

def referanslar(request):
    context = get_common_context()
    # ... diğer context verileri ...
    return render(request, 'referanslar.html', context)

def iletisim(request):
    context = get_common_context()
    # ... diğer context verileri ...
    return render(request, 'iletisim.html', context) 