# Generated by Django 5.1.6 on 2025-03-27 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_siteayarlari_services_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteayarlari',
            name='modern_roof_description',
            field=models.TextField(default='Yenilikçi teknolojiler ve uzman ekibimizle çatınızı geleceğe hazırlıyoruz.', verbose_name='Modern Çatı Açıklama'),
        ),
        migrations.AddField(
            model_name='siteayarlari',
            name='modern_roof_link',
            field=models.URLField(default='#', verbose_name='Modern Çatı Link'),
        ),
        migrations.AddField(
            model_name='siteayarlari',
            name='modern_roof_title',
            field=models.CharField(default='Modern Çatı Sistemleri', max_length=200, verbose_name='Modern Çatı Başlık'),
        ),
    ]
