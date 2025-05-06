from django import forms
from core.models import HeroSection, SiteAyarlari, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class HeroSectionForm(forms.ModelForm):
    class Meta:
        model = HeroSection
        fields = [
            'welcome_text',
            'title',
            'rotating_words',
            'description',
            'background_image',
            'button_text',
            'is_active'
        ]
        widgets = {
            'welcome_text': forms.TextInput(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'rotating_words': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'background_image': forms.FileInput(attrs={
                'class': 'btn btn-primary',
                'style': 'display: none;',
                'accept': 'image/*'
            }),
            'button_text': forms.TextInput(attrs={'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'custom-control-input'})
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_image']
        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control'})
        }

class SiteAyarlariForm(forms.ModelForm):
    class Meta:
        model = SiteAyarlari
        fields = [
            'site_logo', 'footer_logo',
            'menu_anasayfa', 'menu_cati', 'menu_projeler', 'menu_referanslar', 'menu_iletisim',
            'footer_telefon', 'footer_telefon_aktif', 'footer_email', 'footer_email_aktif',
            'footer_adres', 'footer_adres_aktif', 'footer_copyright',
            'mobile_phone', 'mobile_phone_aktif', 'whatsapp', 'whatsapp_aktif',
            'google_maps_url', 'google_maps_url_aktif',
            'facebook', 'facebook_aktif', 'twitter', 'twitter_aktif', 
            'instagram', 'instagram_aktif', 'linkedin', 'linkedin_aktif', 
            'youtube', 'youtube_aktif',
            'footer_description'
        ]
        widgets = {
            'site_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'footer_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'menu_anasayfa': forms.TextInput(attrs={'class': 'form-control'}),
            'menu_cati': forms.TextInput(attrs={'class': 'form-control'}),
            'menu_projeler': forms.TextInput(attrs={'class': 'form-control'}),
            'menu_referanslar': forms.TextInput(attrs={'class': 'form-control'}),
            'menu_iletisim': forms.TextInput(attrs={'class': 'form-control'}),
            'footer_telefon': forms.TextInput(attrs={'class': 'form-control'}),
            'footer_telefon_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'footer_email': forms.EmailInput(attrs={'class': 'form-control'}),
            'footer_email_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'footer_adres': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'footer_adres_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'footer_copyright': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile_phone': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'mobile_phone_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'maxlength': '20'}),
            'whatsapp_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'google_maps_url': forms.URLInput(attrs={'class': 'form-control'}),
            'google_maps_url_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'facebook': forms.URLInput(attrs={'class': 'form-control'}),
            'facebook_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'twitter': forms.URLInput(attrs={'class': 'form-control'}),
            'twitter_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'instagram': forms.URLInput(attrs={'class': 'form-control'}),
            'instagram_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'linkedin': forms.URLInput(attrs={'class': 'form-control'}),
            'linkedin_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'youtube': forms.URLInput(attrs={'class': 'form-control'}),
            'youtube_aktif': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'footer_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
        }

class SifreDegistirForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Mevcut Şifre'
        self.fields['new_password1'].label = 'Yeni Şifre'
        self.fields['new_password2'].label = 'Yeni Şifre (Tekrar)'
        
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'}) 