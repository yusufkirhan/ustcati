from core.models import TeklifTalebi, SiteAyarlari

def yeni_teklif_sayisi(request):
    if request.user.is_authenticated:
        return {
            'yeni_teklif_sayisi': TeklifTalebi.objects.filter(okundu=False).count()
        }
    return {'yeni_teklif_sayisi': 0}

def site_ayarlari(request):
    site_ayarlari, _ = SiteAyarlari.objects.get_or_create(pk=1)
    return {
        'site_ayarlari': site_ayarlari
    } 