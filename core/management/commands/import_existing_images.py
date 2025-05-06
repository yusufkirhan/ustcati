from django.core.management.base import BaseCommand
from django.core.files import File
from core.models import Medya
import os
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = 'Mevcut resimleri medya galerisine aktarır'

    def handle(self, *args, **kwargs):
        # Static klasöründeki resimleri aktar
        static_images_dir = os.path.join(settings.BASE_DIR, 'static', 'images')
        self.import_images_from_directory(static_images_dir, "Static")

        # Media klasöründeki resimleri aktar
        media_dir = os.path.join(settings.BASE_DIR, 'media')
        self.import_images_from_directory(media_dir, "Media")

    def import_images_from_directory(self, directory, source):
        if not os.path.exists(directory):
            self.stdout.write(self.style.WARNING(f'{directory} klasörü bulunamadı'))
            return

        for root, dirs, files in os.walk(directory):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.tif', '.tiff')):
                    file_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(file_path, directory)
                    
                    # Dosya zaten medya galerisinde var mı kontrol et
                    if not Medya.objects.filter(baslik=relative_path).exists():
                        try:
                            with open(file_path, 'rb') as f:
                                medya = Medya()
                                medya.baslik = relative_path
                                medya.resim.save(filename, File(f), save=True)
                                self.stdout.write(self.style.SUCCESS(f'Başarıyla aktarıldı: {relative_path}'))
                        except Exception as e:
                            self.stdout.write(self.style.ERROR(f'Hata: {relative_path} - {str(e)}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Zaten mevcut: {relative_path}')) 