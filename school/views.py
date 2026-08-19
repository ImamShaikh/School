from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.exceptions import ValidationError
from django.utils.html import escape
import re

from Appadmin.models import Teacher, Event, News, GalleryImage, SchoolInfo
from .models import contact, registration

# Helper: context processor fallback for school info
def get_school_info():
    info, created = SchoolInfo.objects.get_or_create(id=1)
    return info

def home(request):
    info = get_school_info()
    teachers = Teacher.objects.all()[:4]
    events = Event.objects.all().order_by('-date')[:3]
    news_list = News.objects.all().order_by('-date')[:3]
    gallery_imgs = GalleryImage.objects.all()[:6]
    
    context = {
        'info': info,
        'teachers': teachers,
        'events': events,
        'news_list': news_list,
        'gallery_imgs': gallery_imgs,
    }
    return render(request, 'index.html', context)

def about(request):
    info = get_school_info()
    return render(request, 'about-us.html', {'info': info})

def teachers_view(request):
    info = get_school_info()
    teachers = Teacher.objects.all()
    return render(request, 'Teachers.html', {'teachers': teachers, 'info': info})

def events_view(request):
    info = get_school_info()
    events = Event.objects.all().order_by('-date')
    return render(request, 'event.html', {'events': events, 'info': info})

def gallery_view(request):
    info = get_school_info()
    gallery_imgs = GalleryImage.objects.all().order_by('-uploaded_at')
    
    # Get unique categories present in gallery
    categories = GalleryImage.objects.values_list('category', flat=True).distinct()
    
    context = {
        'gallery_imgs': gallery_imgs,
        'categories': categories,
        'info': info
    }
    return render(request, 'Gallery.html', context)

def news_view(request):
    info = get_school_info()
    articles_list = News.objects.all().order_by('-date')
    category_filter = request.GET.get('category')
    
    if category_filter and category_filter != 'All':
        articles_list = articles_list.filter(category=category_filter)
        
    paginator = Paginator(articles_list, 6) # 6 articles per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = ['All', 'Admissions', 'Achievements', 'Events', 'Announcements', 'General']
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'selected_category': category_filter or 'All',
        'info': info
    }
    return render(request, 'news.html', context)

def news_detail(request, slug):
    info = get_school_info()
    article = get_object_or_404(News, slug=slug)
    return render(request, 'news_detail.html', {'article': article, 'info': info})

def contact_view(request):
    info = get_school_info()
    if request.method == 'POST':
        # Simple Rate Limiting check
        submissions = request.session.get('contact_submissions', 0)
        if submissions >= 3:
            messages.error(request, "You have exceeded the submission limit. Please try again later.")
            return render(request, 'contact-us.html', {'info': info})
            
        name = escape(request.POST.get('name', '').strip())
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = escape(request.POST.get('message', '').strip())
        
        # Validations
        errors = []
        if not name or len(name) < 2:
            errors.append("Please enter a valid name (min 2 characters).")
        if email:
            if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                errors.append("Please enter a valid email address.")
        if not phone or not phone.isdigit() or len(phone) != 10:
            errors.append("Please enter a valid 10-digit phone number.")
        if not message or len(message) < 10:
            errors.append("Message must be at least 10 characters long.")
            
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'contact-us.html', {'info': info, 'posted': request.POST})
            
        contact.objects.create(name=name, email=email, phone_no=phone, message=message)
        request.session['contact_submissions'] = submissions + 1
        messages.success(request, "✓ Message sent successfully. We will contact you soon.")
        return redirect('school:contact')
        
    return render(request, 'contact-us.html', {'info': info})

def register_view(request):
    info = get_school_info()
    if request.method == 'POST':
        # Simple Rate Limiting check
        submissions = request.session.get('registration_submissions', 0)
        if submissions >= 2:
            messages.error(request, "You have exceeded the submission limit. Please try again later.")
            return render(request, 'registration.html', {'info': info})
            
        # Form Data
        stud_name = escape(request.POST.get('fname', '').strip())
        M_name = escape(request.POST.get('mname', '').strip())
        dob = request.POST.get('dob', '').strip()
        gender = request.POST.get('gender', '').strip()
        religion = escape(request.POST.get('religion', '').strip())
        category = request.POST.get('category', '').strip()
        pob = escape(request.POST.get('pob', '').strip())
        email = request.POST.get('email', '').strip()
        mob = request.POST.get('mob', '').strip()
        p_adhar = request.POST.get('p_adhar', '').strip()
        c_adhar = request.POST.get('c_adhar', '').strip()
        street = escape(request.POST.get('street', '').strip())
        landmark = escape(request.POST.get('landmark', '').strip())
        state = escape(request.POST.get('state', '').strip())
        pin_code = request.POST.get('pincode', '').strip()
        
        # Validations
        errors = []
        if not stud_name or len(stud_name) < 3:
            errors.append("Please enter a valid student name.")
        if not M_name or len(M_name) < 3:
            errors.append("Please enter a valid mother's name.")
        if not dob:
            errors.append("Date of Birth is required.")
        if not gender:
            errors.append("Gender is required.")
        if not mob or not mob.isdigit() or len(mob) != 10:
            errors.append("Please enter a valid 10-digit mobile number.")
        if p_adhar and (not p_adhar.isdigit() or len(p_adhar) != 12):
            errors.append("Parent Aadhar must be exactly 12 digits.")
        if c_adhar and (not c_adhar.isdigit() or len(c_adhar) != 12):
            errors.append("Student Aadhar must be exactly 12 digits.")
        if not pin_code or not pin_code.isdigit() or len(pin_code) != 6:
            errors.append("Please enter a valid 6-digit pin code.")
            
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'registration.html', {'info': info, 'posted': request.POST})
            
        registration.objects.create(
            stud_name=stud_name, M_name=M_name, DOB=dob, gender=gender,
            religion=religion, category=category, P_O_B=pob, email=email,
            M_no=mob, P_adhar=p_adhar, C_adhar=c_adhar, street=street,
            landmark=landmark, state=state, pin_code=int(pin_code)
        )
        
        request.session['registration_submissions'] = submissions + 1
        messages.success(request, "✓ Registration submitted successfully. Your reference code is generated.")
        return redirect('school:register')
        
    return render(request, 'registration.html', {'info': info})
