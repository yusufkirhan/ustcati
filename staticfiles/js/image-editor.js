document.addEventListener('DOMContentLoaded', function() {
    if (document.body.classList.contains('is-admin')) {
        // Resim düzenleme butonlarını ekle
        document.querySelectorAll('img[data-editable="image"]').forEach(function(img) {
            const wrapper = document.createElement('div');
            wrapper.className = 'image-editor-wrapper';
            wrapper.style.position = 'relative';
            
            const editButton = document.createElement('button');
            editButton.className = 'btn btn-sm btn-primary image-edit-button';
            editButton.innerHTML = '<i class="fas fa-edit"></i>';
            editButton.style.position = 'absolute';
            editButton.style.top = '10px';
            editButton.style.right = '10px';
            editButton.setAttribute('aria-label', 'Resmi düzenle');
            
            img.parentNode.insertBefore(wrapper, img);
            wrapper.appendChild(img);
            wrapper.appendChild(editButton);
            
            // Resim yükleme modalını oluştur
            editButton.addEventListener('click', function() {
                const modal = document.createElement('div');
                modal.className = 'modal fade';
                modal.setAttribute('tabindex', '-1');
                modal.setAttribute('role', 'dialog');
                modal.setAttribute('aria-labelledby', 'imageEditModalLabel');
                modal.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="imageEditModalLabel">Resim Yükle</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Kapat"></button>
                            </div>
                            <div class="modal-body">
                                <div class="mb-3">
                                    <label for="imageUpload" class="form-label">Yeni Resim Seç</label>
                                    <input type="file" class="form-control" id="imageUpload" accept="image/*" aria-describedby="imageHelp">
                                    <div id="imageHelp" class="form-text">Maksimum dosya boyutu: 5MB</div>
                                </div>
                                <div class="preview-container mb-3" style="display: none;">
                                    <h6>Önizleme:</h6>
                                    <img src="" class="img-fluid rounded" id="imagePreview" alt="Resim önizleme">
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">İptal</button>
                                <button type="button" class="btn btn-primary" id="saveImage">Kaydet</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(modal);
                const bsModal = new bootstrap.Modal(modal);
                bsModal.show();
                
                // Resim önizleme
                const fileInput = modal.querySelector('#imageUpload');
                const preview = modal.querySelector('#imagePreview');
                const previewContainer = modal.querySelector('.preview-container');
                const saveButton = modal.querySelector('#saveImage');
                
                fileInput.addEventListener('change', function() {
                    if (this.files && this.files[0]) {
                        const file = this.files[0];
                        
                        // Dosya boyutu kontrolü
                        if (file.size > 5 * 1024 * 1024) {
                            alert('Dosya boyutu çok büyük. Maksimum 5MB kabul edilir.');
                            this.value = '';
                            return;
                        }
                        
                        // Dosya tipi kontrolü
                        if (!file.type.startsWith('image/')) {
                            alert('Lütfen sadece resim dosyası seçin.');
                            this.value = '';
                            return;
                        }
                        
                        const reader = new FileReader();
                        reader.onload = function(e) {
                            preview.src = e.target.result;
                            previewContainer.style.display = 'block';
                            saveButton.disabled = false;
                        }
                        reader.readAsDataURL(file);
                    } else {
                        previewContainer.style.display = 'none';
                        saveButton.disabled = true;
                    }
                });
                
                // Kaydet butonu
                saveButton.addEventListener('click', async function() {
                    const formData = new FormData();
                    formData.append('image', fileInput.files[0]);
                    formData.append('field', img.dataset.field);
                    
                    try {
                        saveButton.disabled = true;
                        saveButton.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Yükleniyor...';
                        
                        const response = await fetch('/panel/update-image/', {
                            method: 'POST',
                            body: formData,
                            headers: {
                                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                            }
                        });

                        if (!response.ok) {
                            throw new Error(`HTTP error! status: ${response.status}`);
                        }

                        const contentType = response.headers.get("content-type");
                        if (!contentType || !contentType.includes("application/json")) {
                            throw new Error("Sunucudan JSON yanıtı alınamadı!");
                        }

                        const data = await response.json();
                        
                        if (data.success) {
                            img.src = data.image_url;
                            bsModal.hide();
                            modal.remove();
                            showNotification('Resim başarıyla güncellendi');
                        } else {
                            throw new Error(data.error || 'Resim güncellenirken bir hata oluştu');
                        }
                    } catch (error) {
                        console.error('Hata:', error);
                        showNotification(error.message, 'error');
                    } finally {
                        saveButton.disabled = false;
                        saveButton.innerHTML = 'Kaydet';
                    }
                });
                
                // Modal kapandığında temizlik
                modal.addEventListener('hidden.bs.modal', function() {
                    modal.remove();
                });
            });
        });
    }
});

// Bildirim gösterme fonksiyonu
function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} position-fixed top-0 end-0 m-3`;
    notification.style.zIndex = '9999';
    notification.setAttribute('role', 'alert');
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
} 