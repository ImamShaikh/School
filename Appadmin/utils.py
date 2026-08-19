import os
import uuid
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile
from PIL import Image

def validate_and_save_image(uploaded_file: UploadedFile, max_size_mb=5):
    if not uploaded_file:
        return None
        
    # 1. Check file size
    if uploaded_file.size > max_size_mb * 1024 * 1024:
        raise ValidationError(f"File size exceeds the limit of {max_size_mb} MB.")
    
    # 2. Check extension
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if ext not in valid_extensions:
        raise ValidationError("Unsupported file extension. Only JPG, JPEG, PNG, and WebP are allowed.")
    
    # 3. Validate actual image contents & dimensions using Pillow
    try:
        # Re-open/verify image
        img = Image.open(uploaded_file)
        img.verify()
    except Exception:
        raise ValidationError("Invalid or corrupted image file.")
    
    # Reset file pointer after verification
    uploaded_file.seek(0)
    
    # 4. Double check MIME format
    img = Image.open(uploaded_file)
    mime_type = img.format.lower()
    valid_mime_types = ['jpeg', 'png', 'webp', 'jpg']
    if mime_type not in valid_mime_types:
        raise ValidationError("Invalid image format. Supported formats: JPEG, PNG, WebP.")
        
    # 5. Generate safe filename using UUID
    safe_name = f"{uuid.uuid4().hex}{ext}"
    uploaded_file.name = safe_name
    uploaded_file.seek(0)
    return uploaded_file
