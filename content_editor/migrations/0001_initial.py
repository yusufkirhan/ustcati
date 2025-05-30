# Generated by Django 5.1.6 on 2025-04-22 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteAyarlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hero_title', models.CharField(blank=True, max_length=200, null=True)),
                ('hero_description', models.TextField(blank=True, null=True)),
                ('hero_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('hero_button_text', models.CharField(blank=True, max_length=50, null=True)),
                ('hero_button_link', models.CharField(blank=True, max_length=200, null=True)),
                ('roof_systems_title', models.CharField(blank=True, max_length=200, null=True)),
                ('roof_systems_subtitle', models.TextField(blank=True, null=True)),
                ('roof_systems_hero_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('roof_systems_solutions_title', models.CharField(blank=True, max_length=200, null=True)),
                ('kiremit_cati_title', models.CharField(blank=True, max_length=200, null=True)),
                ('kiremit_cati_description', models.TextField(blank=True, null=True)),
                ('kiremit_cati_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('kiremit_cati_feature1', models.CharField(blank=True, max_length=200, null=True)),
                ('kiremit_cati_feature2', models.CharField(blank=True, max_length=200, null=True)),
                ('kiremit_cati_feature3', models.CharField(blank=True, max_length=200, null=True)),
                ('metal_cati_title', models.CharField(blank=True, max_length=200, null=True)),
                ('metal_cati_description', models.TextField(blank=True, null=True)),
                ('metal_cati_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('metal_cati_feature1', models.CharField(blank=True, max_length=200, null=True)),
                ('metal_cati_feature2', models.CharField(blank=True, max_length=200, null=True)),
                ('metal_cati_feature3', models.CharField(blank=True, max_length=200, null=True)),
                ('shingle_cati_title', models.CharField(blank=True, max_length=200, null=True)),
                ('shingle_cati_description', models.TextField(blank=True, null=True)),
                ('shingle_cati_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('shingle_cati_feature1', models.CharField(blank=True, max_length=200, null=True)),
                ('shingle_cati_feature2', models.CharField(blank=True, max_length=200, null=True)),
                ('shingle_cati_feature3', models.CharField(blank=True, max_length=200, null=True)),
                ('why_choose_title', models.CharField(blank=True, max_length=200, null=True)),
                ('feature1_title', models.CharField(blank=True, max_length=200, null=True)),
                ('feature1_description', models.TextField(blank=True, null=True)),
                ('feature2_title', models.CharField(blank=True, max_length=200, null=True)),
                ('feature2_description', models.TextField(blank=True, null=True)),
                ('feature3_title', models.CharField(blank=True, max_length=200, null=True)),
                ('feature3_description', models.TextField(blank=True, null=True)),
                ('features_image', models.ImageField(blank=True, null=True, upload_to='medya/')),
                ('process_title', models.CharField(blank=True, max_length=200, null=True)),
                ('step1_title', models.CharField(blank=True, max_length=200, null=True)),
                ('step1_description', models.TextField(blank=True, null=True)),
                ('step2_title', models.CharField(blank=True, max_length=200, null=True)),
                ('step2_description', models.TextField(blank=True, null=True)),
                ('step3_title', models.CharField(blank=True, max_length=200, null=True)),
                ('step3_description', models.TextField(blank=True, null=True)),
                ('step4_title', models.CharField(blank=True, max_length=200, null=True)),
                ('step4_description', models.TextField(blank=True, null=True)),
                ('cta_title', models.CharField(blank=True, max_length=200, null=True)),
                ('cta_description', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Site Ayarları',
                'verbose_name_plural': 'Site Ayarları',
            },
        ),
    ]
