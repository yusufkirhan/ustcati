# Generated by Django 5.1.6 on 2025-04-22 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.CharField(choices=[('konut', 'Konut'), ('ticari', 'Ticari'), ('endustriyel', 'Endüstriyel'), ('tumu', 'Tümü')], default='tumu', max_length=20, verbose_name='Kategori'),
        ),
    ]
