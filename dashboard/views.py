from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.http import JsonResponse
from core.models import TeklifTalebi, HeroSection, Medya, Contact, SiteAyarlari, UserProfile
from .models import Blog, Project, Service, Customer, Offer
from django.contrib import messages
from .forms import HeroSectionForm, SiteAyarlariForm, UserProfileForm, SifreDegistirForm
from django.views.decorators.http import require_POST
from django.contrib.auth.forms import PasswordChangeForm
from django.utils import timezone
import os

def get_common_context(request):
    site_ayarlari, _ = SiteAyarlari.objects.get_or_create(pk=1)
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return {
        'site_ayarlari': site_ayarlari,
        'user_profile': user_profile
    }

# Create your views here.

@login_required
def index(request):
    context = get_common_context(request)
    
    # Teklif Talepleri - TeklifTalebi modelinden
    total_offers = TeklifTalebi.objects.all().count()
    
    # İletişim Mesajları - Contact modelinden
    total_messages = Contact.objects.all().count()
    
    # Projeler - Project modelinden
    total_projects = Project.objects.all().count()
    
    # Blog Yazıları - Blog modelinden
    total_posts = Blog.objects.all().count()
    
    # Son projeler
    recent_projects = Project.objects.all().order_by('-created_at')[:5]
    
    # Son aktiviteler
    recent_activities = []
    
    # Son mesajları aktivitelere ekle
    recent_messages = Contact.objects.all().order_by('-created_at')[:3]
    for message in recent_messages:
        recent_activities.append({
            'type': 'mesaj',
            'title': f'Yeni Mesaj: {message.name}',
            'description': message.message[:100] + '...' if len(message.message) > 100 else message.message,
            'time': message.created_at
        })
    
    # Son projeleri aktivitelere ekle
    for project in recent_projects[:3]:
        recent_activities.append({
            'type': 'proje',
            'title': f'Yeni Proje: {project.title}',
            'description': project.description[:100] + '...' if project.description and len(project.description) > 100 else project.description,
            'time': project.created_at
        })
    
    # Son yazıları aktivitelere ekle
    recent_posts = Blog.objects.all().order_by('-created_at')[:3]
    for post in recent_posts:
        recent_activities.append({
            'type': 'yazi',
            'title': f'Yeni Yazı: {post.title}',
            'description': post.content[:100] + '...' if len(post.content) > 100 else post.content,
            'time': post.created_at
        })
    
    # Son teklifleri aktivitelere ekle
    recent_offers = TeklifTalebi.objects.all().order_by('-tarih')[:3]
    for offer in recent_offers:
        recent_activities.append({
            'type': 'teklif',
            'title': f'Yeni Teklif: {offer.ad_soyad}',
            'description': offer.mesaj[:100] + '...' if len(offer.mesaj) > 100 else offer.mesaj,
            'time': offer.tarih
        })
    
    # Aktiviteleri tarihe göre sırala ve son 5 tanesini al
    recent_activities.sort(key=lambda x: x['time'], reverse=True)
    recent_activities = recent_activities[:5]
    
    context.update({
        'total_offers': total_offers,
        'total_messages': total_messages,
        'total_posts': total_posts,
        'total_projects': total_projects,
        'recent_projects': recent_projects,
        'recent_activities': recent_activities
    })
    
    return render(request, 'dashboard/dashboard.html', context)

@login_required
def projeler(request):
    context = get_common_context(request)
    projects = Project.objects.all().order_by('-created_at')
    context['projects'] = projects
    return render(request, 'dashboard/projeler.html', context)

@login_required
def hizmetler(request):
    context = get_common_context(request)
    return render(request, 'dashboard/hizmetler.html', context)

@login_required
def musteriler(request):
    context = get_common_context(request)
    return render(request, 'dashboard/musteriler.html', context)

@login_required
def randevular(request):
    context = get_common_context(request)
    return render(request, 'dashboard/randevular.html', context)

@login_required
def raporlar(request):
    context = get_common_context(request)
    return render(request, 'dashboard/raporlar.html', context)

@login_required
def ayarlar(request):
    # Site ayarlarını al veya oluştur
    site_ayarlari, _ = SiteAyarlari.objects.get_or_create(pk=1)
    
    # Kullanıcı profilini al veya oluştur
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        if form_type == 'site_ayarlari':
            form = SiteAyarlariForm(request.POST, request.FILES, instance=site_ayarlari)
            if form.is_valid():
                # Yeni alanları manuel olarak kaydet
                site_ayarlari.mobile_phone = request.POST.get('mobile_phone', '')
                site_ayarlari.whatsapp = request.POST.get('whatsapp', '')
                site_ayarlari.google_maps_url = request.POST.get('google_maps_url', '')
                site_ayarlari.save()
                
                form.save()
                messages.success(request, 'Site ayarları başarıyla güncellendi.')
                return redirect('dashboard:ayarlar')
            else:
                messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
        
        elif form_type == 'profil':
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                
                user = request.user
                user.first_name = request.POST.get('first_name')
                user.last_name = request.POST.get('last_name')
                user.email = request.POST.get('email')
                user.save()
                
                messages.success(request, 'Profil başarıyla güncellendi.')
                return redirect('dashboard:ayarlar')
            else:
                messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
    
    site_form = SiteAyarlariForm(instance=site_ayarlari)
    profile_form = UserProfileForm(instance=user_profile)
    
    context = {
        'site_form': site_form,
        'profile_form': profile_form,
        'site_ayarlari': site_ayarlari,
        'user_profile': user_profile
    }
    
    return render(request, 'dashboard/ayarlar.html', context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def teklifler(request):
    context = get_common_context(request)
    context['teklifler'] = TeklifTalebi.objects.all().order_by('-tarih')
    return render(request, 'dashboard/teklifler.html', context)

@login_required
def teklif_detay(request, teklif_id):
    try:
        teklif = TeklifTalebi.objects.get(id=teklif_id)
        data = {
            'ad_soyad': teklif.ad_soyad,
            'email': teklif.email,
            'telefon': teklif.telefon,
            'konu': teklif.konu,
            'mesaj': teklif.mesaj,
            'tarih': teklif.tarih.strftime('%d.m.Y %H:%M')
        }
        if not teklif.okundu:
            teklif.okundu = True
            teklif.save()
        return JsonResponse(data)
    except TeklifTalebi.DoesNotExist:
        return JsonResponse({'error': 'Teklif bulunamadı'}, status=404)

@login_required
def teklif_okundu(request, teklif_id):
    try:
        teklif = TeklifTalebi.objects.get(id=teklif_id)
        teklif.okundu = True
        teklif.save()
        return JsonResponse({'status': 'success'})
    except TeklifTalebi.DoesNotExist:
        return JsonResponse({'error': 'Teklif bulunamadı'}, status=404)

@login_required
def teklif_sil(request, teklif_id):
    try:
        teklif = TeklifTalebi.objects.get(id=teklif_id)
        teklif.delete()
        return JsonResponse({'status': 'success'})
    except TeklifTalebi.DoesNotExist:
        return JsonResponse({'error': 'Teklif bulunamadı'}, status=404)

@login_required
@require_POST
def toplu_okundu(request):
    teklif_ids = request.POST.getlist('teklifler[]')
    TeklifTalebi.objects.filter(id__in=teklif_ids).update(okundu=True)
    messages.success(request, 'Seçili teklifler okundu olarak işaretlendi.')
    return JsonResponse({'status': 'success'})

@login_required
@require_POST
def toplu_sil(request):
    teklif_ids = request.POST.getlist('teklifler[]')
    TeklifTalebi.objects.filter(id__in=teklif_ids).delete()
    messages.success(request, 'Seçili teklifler başarıyla silindi.')
    return JsonResponse({'status': 'success'})

@login_required
def hero_section_list(request):
    context = get_common_context(request)
    context['hero_sections'] = HeroSection.objects.all().order_by('order', '-created_at')
    return render(request, 'dashboard/hero_section.html', context)

@login_required
def hero_section_create(request):
    context = get_common_context(request)
    if request.method == 'POST':
        form = HeroSectionForm(request.POST, request.FILES)
        if form.is_valid():
            hero_section = form.save(commit=False)
            
            # Medya galerisinden seçilen resmi kontrol et
            background_image_id = request.POST.get('background_image_id')
            if background_image_id:
                try:
                    media = Medya.objects.get(id=background_image_id)
                    if media.resim:
                        hero_section.background_image = media.resim
                except Medya.DoesNotExist:
                    messages.error(request, 'Seçilen medya bulunamadı.')
                    return render(request, 'dashboard/hero_section_form.html', context)
            
            hero_section.save()
            messages.success(request, 'Hero section başarıyla oluşturuldu.')
            return redirect('dashboard:hero_section_list')
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = HeroSectionForm()
    
    context['form'] = form
    context['medya_list'] = Medya.objects.all().order_by('-yukleme_tarihi')
    return render(request, 'dashboard/hero_section_form.html', context)

@login_required
def hero_section_edit(request, pk):
    context = get_common_context(request)
    try:
        hero_section = HeroSection.objects.get(id=pk)
    except HeroSection.DoesNotExist:
        messages.error(request, 'Hero section bulunamadı.')
        return redirect('dashboard:hero_section_list')
    
    if request.method == 'POST':
        form = HeroSectionForm(request.POST, request.FILES, instance=hero_section)
        if form.is_valid():
            hero_section = form.save(commit=False)
            
            # Medya galerisinden seçilen resmi kontrol et
            background_image_id = request.POST.get('background_image_id')
            if background_image_id:
                try:
                    media = Medya.objects.get(id=background_image_id)
                    if media.resim:
                        hero_section.background_image = media.resim
                except Medya.DoesNotExist:
                    messages.error(request, 'Seçilen medya bulunamadı.')
                    return render(request, 'dashboard/hero_section_form.html', context)
            
            hero_section.save()
            messages.success(request, 'Hero section başarıyla güncellendi.')
            return redirect('dashboard:hero_section_list')
        else:
            messages.error(request, 'Lütfen formu doğru şekilde doldurun.')
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = HeroSectionForm(instance=hero_section)
    
    context['form'] = form
    context['hero_section'] = hero_section
    context['medya_list'] = Medya.objects.all().order_by('-yukleme_tarihi')
    return render(request, 'dashboard/hero_section_form.html', context)

@login_required
def hero_section_delete(request, pk):
    hero = get_object_or_404(HeroSection, pk=pk)
    try:
        hero.delete()
        messages.success(request, 'Hero section başarıyla silindi.')
    except Exception as e:
        messages.error(request, f'Bir hata oluştu: {str(e)}')
    return redirect('dashboard:hero_section_list')

@login_required
def medya_listesi(request):
    if request.GET.get('format') == 'json':
        medya_list = Medya.objects.all().order_by('-yukleme_tarihi')
        data = []
        for medya in medya_list:
            data.append({
                'id': medya.id,
                'baslik': medya.baslik,
                'resim': medya.resim.url if medya.resim else None,
                'yukleme_tarihi': medya.yukleme_tarihi.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse(data, safe=False)
    
    context = get_common_context(request)
    medya_list = Medya.objects.all().order_by('-yukleme_tarihi')
    context['medya_list'] = medya_list
    return render(request, 'dashboard/medya.html', context)

@login_required
def medya_yukle(request):
    if request.method == 'POST':
        try:
            Medya.objects.create(
                baslik=request.POST.get('baslik'),
                resim=request.FILES.get('resim')
            )
            messages.success(request, 'Resim başarıyla yüklendi.')
        except Exception as e:
            messages.error(request, f'Bir hata oluştu: {str(e)}')
    return redirect('dashboard:medya_listesi')

@login_required
def medya_sil(request, pk):
    try:
        medya = Medya.objects.get(pk=pk)
        medya.delete()  # Bu artık fiziksel dosyayı da silecek
        messages.success(request, 'Medya başarıyla silindi.')
    except Medya.DoesNotExist:
        messages.error(request, 'Medya bulunamadı.')
    except Exception as e:
        messages.error(request, f'Silme işlemi sırasında bir hata oluştu: {str(e)}')
    return redirect('dashboard:medya_listesi')

@login_required
def mesajlar(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('login')
    
    messages = Contact.objects.all().order_by('-created_at')
    context = {
        'messages': messages
    }
    return render(request, 'dashboard/mesajlar.html', context)

@login_required
def mesaj_detay(request, mesaj_id):
    context = get_common_context(request)
    context['mesaj'] = get_object_or_404(Contact, id=mesaj_id)
    if not context['mesaj'].is_read:
        context['mesaj'].is_read = True
        context['mesaj'].save()
    return render(request, 'dashboard/mesajlar/detay.html', context)

@login_required
def mesaj_durum_guncelle(request, mesaj_id):
    if request.method == 'POST':
        mesaj = get_object_or_404(Contact, id=mesaj_id)
        yeni_durum = request.POST.get('status')
        if yeni_durum in ['pending', 'processed', 'answered']:
            mesaj.status = yeni_durum
            mesaj.save()
            messages.success(request, 'Mesaj durumu güncellendi.')
        return redirect('dashboard:mesaj_detay', mesaj_id=mesaj_id)
    return redirect('dashboard:mesajlar')

@login_required
def mesaj_sil(request, mesaj_id):
    mesaj = get_object_or_404(Contact, id=mesaj_id)
    mesaj.delete()
    messages.success(request, 'Mesaj başarıyla silindi.')
    return redirect('dashboard:mesajlar')

@login_required
def profil_guncelle(request):
    if request.method == 'POST':
        user = request.user
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        messages.success(request, 'Profil başarıyla güncellendi.')
        return redirect('dashboard:ayarlar')
    return redirect('dashboard:ayarlar')

@login_required
def sifre_degistir(request):
    if request.method == 'POST':
        form = SifreDegistirForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Şifreniz başarıyla değiştirildi!')
            return redirect('dashboard:sifre_degistir')
        else:
            messages.error(request, 'Lütfen hataları düzeltin.')
    else:
        form = SifreDegistirForm(request.user)
    
    return render(request, 'dashboard/sifre_degistir.html', {
        'form': form
    })

@login_required
@require_POST
def update_image(request):
    try:
        field = request.POST.get('field')
        image = request.FILES.get('image')
        
        if not field or not image:
            return JsonResponse({
                'success': False,
                'error': 'Eksik parametreler: field ve image gerekli'
            }, status=400)
        
        # Site ayarlarını al veya oluştur
        site_ayarlari, created = SiteAyarlari.objects.get_or_create(pk=1)
        
        # Dosya tipini kontrol et
        if not image.content_type.startswith('image/'):
            return JsonResponse({
                'success': False,
                'error': 'Geçersiz dosya tipi. Sadece resim dosyaları kabul edilir.'
            }, status=400)
        
        # Dosya boyutunu kontrol et (örneğin 5MB)
        if image.size > 5 * 1024 * 1024:
            return JsonResponse({
                'success': False,
                'error': 'Dosya boyutu çok büyük. Maksimum 5MB kabul edilir.'
            }, status=400)
        
        setattr(site_ayarlari, field, image)
        site_ayarlari.save()
        
        return JsonResponse({
            'success': True,
            'image_url': getattr(site_ayarlari, field).url
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

@login_required
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'dashboard/blog/list.html', {'blogs': blogs})

@login_required
def blog_ekle(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if title and content and image:
            blog = Blog.objects.create(
                title=title,
                content=content,
                image=image
            )
            messages.success(request, 'Blog yazısı başarıyla eklendi.')
            return redirect('dashboard:blog_list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    return render(request, 'dashboard/blog/ekle.html')

@login_required
def blog_duzenle(request, id):
    blog = get_object_or_404(Blog, id=id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        
        if title and content:
            blog.title = title
            blog.content = content
            if image:
                blog.image = image
            blog.save()
            messages.success(request, 'Blog yazısı başarıyla güncellendi.')
            return redirect('dashboard:blog_list')
        else:
            messages.error(request, 'Lütfen tüm alanları doldurun.')
    
    return render(request, 'dashboard/blog/duzenle.html', {'blog': blog})

@login_required
def blog_sil(request, id):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    messages.success(request, 'Blog yazısı başarıyla silindi.')
    return redirect('dashboard:blog_list')

@login_required
def proje_listesi(request):
    context = get_common_context(request)
    projects = Project.objects.all().order_by('-created_at')
    context['projects'] = projects
    return render(request, 'dashboard/projeler.html', context)

@login_required
def proje_ekle(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
        
    if request.method == 'POST':
        try:
            # is_active değerini düzgün şekilde işle
            is_active = request.POST.get('is_active', '') == 'on'
            
            proje = Project.objects.create(
                title=request.POST.get('title'),
                description=request.POST.get('description'),
                image=request.FILES.get('image'),
                completion_date=request.POST.get('completion_date'),
                location=request.POST.get('location'),
                client=request.POST.get('client'),
                is_active=is_active
            )
            messages.success(request, 'Proje başarıyla eklendi.')
            return redirect('dashboard:proje_listesi')
        except Exception as e:
            messages.error(request, f'Proje eklenirken bir hata oluştu: {str(e)}')
    
    return render(request, 'dashboard/proje_ekle.html')

@login_required
def proje_duzenle(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
        
    proje = get_object_or_404(Project, id=id)
    
    if request.method == 'POST':
        try:
            # is_active değerini düzgün şekilde işle
            is_active = request.POST.get('is_active', '') == 'on'
            
            proje.title = request.POST.get('title')
            proje.description = request.POST.get('description')
            if request.FILES.get('image'):
                proje.image = request.FILES.get('image')
            proje.completion_date = request.POST.get('completion_date')
            proje.location = request.POST.get('location')
            proje.client = request.POST.get('client')
            proje.is_active = is_active
            proje.save()
            
            messages.success(request, 'Proje başarıyla güncellendi.')
            return redirect('dashboard:proje_listesi')
        except Exception as e:
            messages.error(request, f'Proje güncellenirken bir hata oluştu: {str(e)}')
    
    return render(request, 'dashboard/proje_duzenle.html', {'proje': proje})

@login_required
def proje_sil(request, id):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('admin:login')
        
    proje = get_object_or_404(Project, id=id)
    
    try:
        proje.delete()
        messages.success(request, 'Proje başarıyla silindi.')
    except Exception as e:
        messages.error(request, f'Proje silinirken bir hata oluştu: {str(e)}')
    
    return redirect('dashboard:proje_listesi')
