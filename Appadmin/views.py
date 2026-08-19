from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils.text import slugify

from school.models import contact, registration
from Appadmin.models import Teacher, Event, News, GalleryImage, SchoolInfo, UserProfile
from Appadmin.utils import validate_and_save_image

# Custom Decorator for Superuser Check
def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            messages.error(request, "Access denied. Superuser privilege required.")
            return redirect('Appadmin:dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Custom Decorator for Staff Check
def staff_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            messages.error(request, "Access denied. Staff privilege required.")
            return redirect('Appadmin:login')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

# Auth Views
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('Appadmin:dashboard')
        
    if request.method == 'POST':
        # Rate limiting block (session-based)
        failed_attempts = request.session.get('login_failures', 0)
        if failed_attempts >= 5:
            messages.error(request, "Too many failed attempts. Please try again later.")
            return render(request, 'Admin/login.html')

        user_in = request.POST.get('username')
        pass_in = request.POST.get('password')
        
        # Authentication
        user = authenticate(request, username=user_in, password=pass_in)
        if user is not None:
            if user.is_staff:
                login(request, user)
                request.session['login_failures'] = 0  # reset failures
                messages.success(request, f"Welcome back, {user.username}!")
                return redirect('Appadmin:dashboard')
            else:
                messages.error(request, "Account is not authorized to access the dashboard.")
        else:
            request.session['login_failures'] = failed_attempts + 1
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'Admin/login.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out successfully.")
    return redirect('Appadmin:login')

# Dashboard View
@staff_required
def dashboard(request):
    total_registrations = registration.objects.count()
    total_messages = contact.objects.count()
    total_teachers = Teacher.objects.count()
    total_events = Event.objects.count()
    total_news = News.objects.count()
    total_gallery = GalleryImage.objects.count()
    
    recent_regs = registration.objects.order_by('-created_at')[:5]
    recent_msgs = contact.objects.order_by('-created_at')[:5]
    upcoming_events = Event.objects.order_by('date')[:5]
    latest_news = News.objects.order_by('-date')[:5]
    
    context = {
        'total_registrations': total_registrations,
        'total_messages': total_messages,
        'total_teachers': total_teachers,
        'total_events': total_events,
        'total_news': total_news,
        'total_gallery': total_gallery,
        'recent_regs': recent_regs,
        'recent_msgs': recent_msgs,
        'upcoming_events': upcoming_events,
        'latest_news': latest_news,
    }
    return render(request, 'Admin/dash.html', context)

# --- Teachers CRUD ---
@staff_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'Admin/teachers_list.html', {'teachers': teachers})

@staff_required
def teacher_add(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subject = request.POST.get('subject')
        expertise = request.POST.get('expertise')
        p_no = request.POST.get('contact')
        qualification = request.POST.get('qualification')
        experience = request.POST.get('experience')
        bio = request.POST.get('bio')
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/teacher_form.html')

        Teacher.objects.create(
            name=name, teach_sub=subject, expertise=expertise, 
            p_no=p_no, qualification=qualification, 
            experience=experience, bio=bio, image=img
        )
        messages.success(request, "Teacher added successfully.")
        return redirect('Appadmin:teacher-list')
        
    return render(request, 'Admin/teacher_form.html')

@staff_required
def teacher_edit(request, id):
    teacher = get_object_or_404(Teacher, id=id)
    if request.method == 'POST':
        teacher.name = request.POST.get('name')
        teacher.teach_sub = request.POST.get('subject')
        teacher.expertise = request.POST.get('expertise')
        teacher.p_no = request.POST.get('contact')
        teacher.qualification = request.POST.get('qualification')
        teacher.experience = request.POST.get('experience')
        teacher.bio = request.POST.get('bio')
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
                teacher.image = img
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/teacher_form.html', {'teacher': teacher})
                
        teacher.save()
        messages.success(request, "Teacher updated successfully.")
        return redirect('Appadmin:teacher-list')
        
    return render(request, 'Admin/teacher_form.html', {'teacher': teacher})

@staff_required
def teacher_delete(request, id):
    if request.method == 'POST':
        teacher = get_object_or_404(Teacher, id=id)
        teacher.delete()
        messages.success(request, "Teacher deleted successfully.")
    return redirect('Appadmin:teacher-list')


# --- Events CRUD ---
@staff_required
def event_list(request):
    events = Event.objects.all().order_by('-date')
    return render(request, 'Admin/events_list.html', {'events': events})

@staff_required
def event_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        date = request.POST.get('date')
        time = request.POST.get('time')
        venue = request.POST.get('venue')
        description = request.POST.get('description')
        reg_info = request.POST.get('reg_info')
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/event_form.html')
                
        Event.objects.create(
            title=title, date=date, time=time, venue=venue,
            description=description, registration_info=reg_info, image=img
        )
        messages.success(request, "Event added successfully.")
        return redirect('Appadmin:event-list')
        
    return render(request, 'Admin/event_form.html')

@staff_required
def event_edit(request, id):
    event = get_object_or_404(Event, id=id)
    if request.method == 'POST':
        event.title = request.POST.get('title')
        event.date = request.POST.get('date')
        event.time = request.POST.get('time')
        event.venue = request.POST.get('venue')
        event.description = request.POST.get('description')
        event.registration_info = request.POST.get('reg_info')
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
                event.image = img
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/event_form.html', {'event': event})
                
        event.save()
        messages.success(request, "Event updated successfully.")
        return redirect('Appadmin:event-list')
        
    return render(request, 'Admin/event_form.html', {'event': event})

@staff_required
def event_delete(request, id):
    if request.method == 'POST':
        event = get_object_or_404(Event, id=id)
        event.delete()
        messages.success(request, "Event deleted successfully.")
    return redirect('Appadmin:event-list')


# --- News CRUD ---
@staff_required
def news_list(request):
    news = News.objects.all().order_by('-date')
    return render(request, 'Admin/news_list.html', {'news': news})

@staff_required
def news_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        summary = request.POST.get('summary')
        content = request.POST.get('content')
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/news_form.html')
                
        News.objects.create(
            title=title, category=category, summary=summary,
            content=content, image=img
        )
        messages.success(request, "News article published.")
        return redirect('Appadmin:news-list')
        
    return render(request, 'Admin/news_form.html')

@staff_required
def news_edit(request, id):
    article = get_object_or_404(News, id=id)
    if request.method == 'POST':
        article.title = request.POST.get('title')
        article.category = request.POST.get('category')
        article.summary = request.POST.get('summary')
        article.content = request.POST.get('content')
        article.slug = slugify(article.title)
        
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
                article.image = img
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return render(request, 'Admin/news_form.html', {'article': article})
                
        article.save()
        messages.success(request, "News article updated.")
        return redirect('Appadmin:news-list')
        
    return render(request, 'Admin/news_form.html', {'article': article})

@staff_required
def news_delete(request, id):
    if request.method == 'POST':
        article = get_object_or_404(News, id=id)
        article.delete()
        messages.success(request, "News article deleted.")
    return redirect('Appadmin:news-list')


# --- Gallery CRUD ---
@staff_required
def gallery_list(request):
    images = GalleryImage.objects.all().order_by('-uploaded_at')
    return render(request, 'Admin/gallery_list.html', {'images': images})

@staff_required
def gallery_add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        category = request.POST.get('category')
        img = request.FILES.get('image')
        if img:
            try:
                img = validate_and_save_image(img)
            except ValidationError as e:
                messages.error(request, f"Image upload error: {e.message}")
                return redirect('Appadmin:gallery-list')
                
            GalleryImage.objects.create(title=title, category=category, image=img)
            messages.success(request, "Gallery image added.")
        else:
            messages.error(request, "Please choose an image file.")
    return redirect('Appadmin:gallery-list')

@staff_required
def gallery_delete(request, id):
    if request.method == 'POST':
        image = get_object_or_404(GalleryImage, id=id)
        image.delete()
        messages.success(request, "Gallery image deleted.")
    return redirect('Appadmin:gallery-list')


# --- Registration Management ---
@staff_required
def registration_list(request):
    regs = registration.objects.all().order_by('-created_at')
    return render(request, 'Admin/registrations_list.html', {'regs': regs})

@staff_required
def registration_status_update(request, id, status):
    if request.method == 'POST':
        reg = get_object_or_404(registration, id=id)
        if status in ['Approved', 'Pending', 'Rejected']:
            reg.status = status
            reg.save()
            messages.success(request, f"Registration for {reg.stud_name} set to {status}.")
    return redirect('Appadmin:registration-list')

@staff_required
def registration_delete(request, id):
    if request.method == 'POST':
        reg = get_object_or_404(registration, id=id)
        reg.delete()
        messages.success(request, "Registration record deleted.")
    return redirect('Appadmin:registration-list')


# --- Messages/Contacts ---
@staff_required
def message_list(request):
    msgs = contact.objects.all().order_by('-created_at')
    return render(request, 'Admin/messages_list.html', {'msgs': msgs})

@staff_required
def message_read_toggle(request, id):
    if request.method == 'POST':
        msg = get_object_or_404(contact, id=id)
        msg.is_read = not msg.is_read
        msg.save()
        status_str = "Read" if msg.is_read else "Unread"
        messages.success(request, f"Message marked as {status_str}.")
    return redirect('Appadmin:message-list')

@staff_required
def message_delete(request, id):
    if request.method == 'POST':
        msg = get_object_or_404(contact, id=id)
        msg.delete()
        messages.success(request, "Message deleted.")
    return redirect('Appadmin:message-list')


# --- School Info Edit ---
@staff_required
def school_info_edit(request):
    info, created = SchoolInfo.objects.get_or_create(id=1)
    if request.method == 'POST':
        info.name = request.POST.get('name')
        info.address = request.POST.get('address')
        info.phone = request.POST.get('phone')
        info.email = request.POST.get('email')
        info.office_hours = request.POST.get('office_hours')
        info.vision = request.POST.get('vision')
        info.mission = request.POST.get('mission')
        info.history = request.POST.get('history')
        info.achievements = request.POST.get('achievements')
        info.principal_name = request.POST.get('principal_name')
        info.principal_message = request.POST.get('principal_message')
        info.facebook = request.POST.get('facebook')
        info.instagram = request.POST.get('instagram')
        info.youtube = request.POST.get('youtube')
        
        logo = request.FILES.get('logo')
        if logo:
            try:
                logo = validate_and_save_image(logo)
                info.logo = logo
            except ValidationError as e:
                messages.error(request, f"Logo upload error: {e.message}")
                
        p_photo = request.FILES.get('principal_photo')
        if p_photo:
            try:
                p_photo = validate_and_save_image(p_photo)
                info.principal_photo = p_photo
            except ValidationError as e:
                messages.error(request, f"Principal photo upload error: {e.message}")
                
        info.save()
        messages.success(request, "School information updated successfully.")
        return redirect('Appadmin:dashboard')
        
    return render(request, 'Admin/school_info_form.html', {'info': info})


# --- Dashboard Users (Superuser only) ---
@superuser_required
def user_list(request):
    users = User.objects.all().select_related('profile')
    return render(request, 'Admin/user_list.html', {'users': users})

@superuser_required
def user_add(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        
        phone = request.POST.get('phone_no')
        address = request.POST.get('address')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'Admin/user_form.html')
            
        new_user = User.objects.create_user(
            username=username, email=email, password=password,
            first_name=first_name, last_name=last_name,
            is_staff=True, is_superuser=False  # Added as Trusted Editor
        )
        
        profile = new_user.profile
        profile.phone_no = phone
        profile.address = address
        profile.save()
        
        messages.success(request, f"Trusted User '{username}' created successfully.")
        return redirect('Appadmin:user-list')
        
    return render(request, 'Admin/user_form.html')

@superuser_required
def user_edit(request, id):
    edit_user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        edit_user.email = request.POST.get('email')
        edit_user.first_name = request.POST.get('first_name')
        edit_user.last_name = request.POST.get('last_name')
        
        password = request.POST.get('password')
        if password:
            edit_user.set_password(password)
            
        edit_user.save()
        
        profile = edit_user.profile
        profile.phone_no = request.POST.get('phone_no')
        profile.address = request.POST.get('address')
        profile.save()
        
        messages.success(request, f"User '{edit_user.username}' details updated.")
        return redirect('Appadmin:user-list')
        
    return render(request, 'Admin/user_form.html', {'edit_user': edit_user})

@superuser_required
def user_delete(request, id):
    if request.method == 'POST':
        del_user = get_object_or_404(User, id=id)
        if del_user == request.user:
            messages.error(request, "You cannot delete your own account.")
        else:
            del_user.delete()
            messages.success(request, "User deleted successfully.")
    return redirect('Appadmin:user-list')
