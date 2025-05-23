# Generated by Django 5.1.6 on 2025-03-27 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_siteayarlari_userprofile'),
    ]

    operations = [
        migrations.CreateModel(
            name='PageContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=100, unique=True)),
                ('content_type', models.CharField(choices=[('text', 'Metin'), ('image', 'Görsel'), ('link', 'Link')], max_length=10)),
                ('content', models.TextField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='page_contents/')),
                ('link_url', models.URLField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sayfa İçeriği',
                'verbose_name_plural': 'Sayfa İçerikleri',
            },
        ),
    ]
