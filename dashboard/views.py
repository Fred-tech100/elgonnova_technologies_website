from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Count, Sum
from core.models import *
from core.forms import *
from django.http import JsonResponse

# Helper function for admin check
def admin_required(user):
    return user.is_superuser or user.is_staff

# Team Members Management
@login_required
@user_passes_test(admin_required)
def dashboard_team(request):
    team_members = TeamMember.objects.all().order_by('order')
    
    if request.method == 'POST':
        if 'add_team' in request.POST:
            TeamMember.objects.create(
                name=request.POST.get('name'),
                position=request.POST.get('position'),
                bio=request.POST.get('bio'),
                quote=request.POST.get('quote'),
                avatar_initial=request.POST.get('avatar_initial'),
                order=request.POST.get('order', 0),
                is_active=request.POST.get('is_active') == 'on',
                social_linkedin=request.POST.get('social_linkedin'),
                social_twitter=request.POST.get('social_twitter'),
                social_github=request.POST.get('social_github')
            )
            if request.FILES.get('image'):
                member = TeamMember.objects.latest('id')
                member.image = request.FILES['image']
                member.save()
            messages.success(request, 'Team member added successfully!')
        elif 'edit_team' in request.POST:
            team_id = request.POST.get('team_id')
            member = get_object_or_404(TeamMember, id=team_id)
            member.name = request.POST.get('name')
            member.position = request.POST.get('position')
            member.bio = request.POST.get('bio')
            member.quote = request.POST.get('quote')
            member.avatar_initial = request.POST.get('avatar_initial')
            member.order = request.POST.get('order', 0)
            member.is_active = request.POST.get('is_active') == 'on'
            member.social_linkedin = request.POST.get('social_linkedin')
            member.social_twitter = request.POST.get('social_twitter')
            member.social_github = request.POST.get('social_github')
            if request.FILES.get('image'):
                member.image = request.FILES['image']
            member.save()
            messages.success(request, 'Team member updated successfully!')
        elif 'delete_team' in request.POST:
            team_id = request.POST.get('team_id')
            TeamMember.objects.filter(id=team_id).delete()
            messages.success(request, 'Team member deleted successfully!')
        return redirect('dashboard_team')
    
    return render(request, 'dashboard/team.html', {'team_members': team_members})
@login_required
@user_passes_test(admin_required)
def get_team_member_api(request, id):
    member = get_object_or_404(TeamMember, id=id)
    data = {
        'id': member.id,
        'name': member.name,
        'position': member.position,
        'avatar_initial': member.avatar_initial,
        'order': member.order,
        'bio': member.bio,
        'quote': member.quote,
        'social_linkedin': member.social_linkedin,
        'social_twitter': member.social_twitter,
        'social_github': member.social_github,
        'is_active': member.is_active,
    }
    return JsonResponse(data)
# Careers Management
@login_required
@user_passes_test(admin_required)
def dashboard_careers(request):
    careers = Career.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        if 'add_career' in request.POST:
            Career.objects.create(
                title=request.POST.get('title'),
                slug=request.POST.get('slug'),
                job_type=request.POST.get('job_type'),
                experience_level=request.POST.get('experience_level'),
                location=request.POST.get('location'),
                salary_range=request.POST.get('salary_range'),
                description=request.POST.get('description'),
                requirements=request.POST.get('requirements'),
                responsibilities=request.POST.get('responsibilities'),
                benefits=request.POST.get('benefits'),
                is_active=request.POST.get('is_active') == 'on',
                is_featured=request.POST.get('is_featured') == 'on',
                application_deadline=request.POST.get('application_deadline') or None
            )
            messages.success(request, 'Job posting added successfully!')
        elif 'edit_career' in request.POST:
            career_id = request.POST.get('career_id')
            career = get_object_or_404(Career, id=career_id)
            career.title = request.POST.get('title')
            career.slug = request.POST.get('slug')
            career.job_type = request.POST.get('job_type')
            career.experience_level = request.POST.get('experience_level')
            career.location = request.POST.get('location')
            career.salary_range = request.POST.get('salary_range')
            career.description = request.POST.get('description')
            career.requirements = request.POST.get('requirements')
            career.responsibilities = request.POST.get('responsibilities')
            career.benefits = request.POST.get('benefits')
            career.is_active = request.POST.get('is_active') == 'on'
            career.is_featured = request.POST.get('is_featured') == 'on'
            career.application_deadline = request.POST.get('application_deadline') or None
            career.save()
            messages.success(request, 'Job posting updated successfully!')
        elif 'delete_career' in request.POST:
            career_id = request.POST.get('career_id')
            Career.objects.filter(id=career_id).delete()
            messages.success(request, 'Job posting deleted successfully!')
        return redirect('dashboard_careers')
    
    return render(request, 'dashboard/careers.html', {'careers': careers})

# Job Applications Management
@login_required
@user_passes_test(admin_required)
def dashboard_applications(request):
    applications = JobApplication.objects.all().order_by('-applied_at')
    
    if request.method == 'POST':
        application_id = request.POST.get('application_id')
        status = request.POST.get('status')
        application = get_object_or_404(JobApplication, id=application_id)
        application.status = status
        application.is_read = True
        application.save()
        messages.success(request, 'Application status updated!')
        return redirect('dashboard_applications')
    
    return render(request, 'dashboard/applications.html', {'applications': applications})

# CEO Message Management
@login_required
@user_passes_test(admin_required)
def dashboard_ceo_message(request):
    ceo_message = CEOMessage.objects.first()
    if not ceo_message:
        ceo_message = CEOMessage.objects.create()
    
    if request.method == 'POST':
        ceo_message.name = request.POST.get('name')
        ceo_message.title = request.POST.get('title')
        ceo_message.message = request.POST.get('message')
        ceo_message.quote = request.POST.get('quote')
        ceo_message.avatar_initial = request.POST.get('avatar_initial')
        ceo_message.is_active = request.POST.get('is_active') == 'on'
        if request.FILES.get('image'):
            ceo_message.image = request.FILES['image']
        ceo_message.save()
        messages.success(request, 'CEO message updated successfully!')
        return redirect('dashboard_ceo_message')
    
    return render(request, 'dashboard/ceo_message.html', {'ceo_message': ceo_message})

# Dashboard Login View
def dashboard_login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        else:
            messages.error(request, 'Invalid credentials or insufficient permissions')
    return render(request, 'dashboard/login.html')

# Dashboard Logout View
@login_required
@user_passes_test(admin_required)
def dashboard_logout_view(request):
    logout(request)
    return redirect('dashboard_login')

# Dashboard Home
@login_required
@user_passes_test(admin_required)
def dashboard_home(request):
    total_messages = ContactMessage.objects.count()
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    total_subscribers = NewsletterSubscriber.objects.count()
    total_blog_posts = BlogPost.objects.count()
    total_portfolio = Portfolio.objects.count()
    total_applications = JobApplication.objects.count()
    total_careers = Career.objects.filter(is_active=True).count()
    
    recent_messages = ContactMessage.objects.order_by('-created_at')[:5]
    recent_subscribers = NewsletterSubscriber.objects.order_by('-subscribed_at')[:5]
    recent_applications = JobApplication.objects.order_by('-applied_at')[:5]
    
    context = {
        'total_messages': total_messages,
        'unread_messages': unread_messages,
        'total_subscribers': total_subscribers,
        'total_blog_posts': total_blog_posts,
        'total_portfolio': total_portfolio,
        'total_applications': total_applications,
        'total_careers': total_careers,
        'recent_messages': recent_messages,
        'recent_subscribers': recent_subscribers,
        'recent_applications': recent_applications,
    }
    return render(request, 'dashboard/index.html', context)

# Blog Posts Management
@login_required
@user_passes_test(admin_required)
def dashboard_posts(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'dashboard/posts.html', {'posts': posts})

@login_required
@user_passes_test(admin_required)
def add_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        category = request.POST.get('category')
        excerpt = request.POST.get('excerpt')
        content = request.POST.get('content')
        icon = request.POST.get('icon')
        is_published = request.POST.get('is_published') == 'on'
        
        post = BlogPost.objects.create(
            title=title,
            slug=slug,
            category=category,
            excerpt=excerpt,
            content=content,
            icon=icon,
            author=request.user,
            is_published=is_published
        )
        
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']
            post.save()
        
        messages.success(request, 'Blog post created successfully!')
        return redirect('dashboard_posts')
    
    return render(request, 'dashboard/add_post.html')

@login_required
@user_passes_test(admin_required)
def edit_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.slug = request.POST.get('slug')
        post.category = request.POST.get('category')
        post.excerpt = request.POST.get('excerpt')
        post.content = request.POST.get('content')
        post.icon = request.POST.get('icon')
        post.is_published = request.POST.get('is_published') == 'on'
        
        if request.FILES.get('featured_image'):
            post.featured_image = request.FILES['featured_image']
        
        post.save()
        messages.success(request, 'Blog post updated successfully!')
        return redirect('dashboard_posts')
    
    return render(request, 'dashboard/edit_post.html', {'post': post})

@login_required
@user_passes_test(admin_required)
def delete_post(request, id):
    post = get_object_or_404(BlogPost, id=id)
    post.delete()
    messages.success(request, 'Blog post deleted successfully!')
    return redirect('dashboard_posts')

# Services Management
@login_required
@user_passes_test(admin_required)
def dashboard_services(request):
    services = Service.objects.all().order_by('order')
    
    if request.method == 'POST':
        if 'add_service' in request.POST:
            Service.objects.create(
                name=request.POST.get('name'),
                icon=request.POST.get('icon'),
                description=request.POST.get('description'),
                order=request.POST.get('order', 0),
                is_active=request.POST.get('is_active') == 'on'
            )
            messages.success(request, 'Service added successfully!')
        elif 'edit_service' in request.POST:
            service_id = request.POST.get('service_id')
            service = get_object_or_404(Service, id=service_id)
            service.name = request.POST.get('name')
            service.icon = request.POST.get('icon')
            service.description = request.POST.get('description')
            service.order = request.POST.get('order', 0)
            service.is_active = request.POST.get('is_active') == 'on'
            service.save()
            messages.success(request, 'Service updated successfully!')
        elif 'delete_service' in request.POST:
            service_id = request.POST.get('service_id')
            Service.objects.filter(id=service_id).delete()
            messages.success(request, 'Service deleted successfully!')
        return redirect('dashboard_services')
    
    return render(request, 'dashboard/services.html', {'services': services})

# Portfolio Management
@login_required
@user_passes_test(admin_required)
def dashboard_portfolio(request):
    portfolio_items = Portfolio.objects.all().order_by('order')
    
    if request.method == 'POST':
        if 'add_portfolio' in request.POST:
            Portfolio.objects.create(
                title=request.POST.get('title'),
                category=request.POST.get('category'),
                icon=request.POST.get('icon'),
                description=request.POST.get('description'),
                technologies=request.POST.get('technologies'),
                project_url=request.POST.get('project_url'),
                is_featured=request.POST.get('is_featured') == 'on',
                order=request.POST.get('order', 0)
            )
            messages.success(request, 'Portfolio item added successfully!')
        elif 'edit_portfolio' in request.POST:
            portfolio_id = request.POST.get('portfolio_id')
            portfolio = get_object_or_404(Portfolio, id=portfolio_id)
            portfolio.title = request.POST.get('title')
            portfolio.category = request.POST.get('category')
            portfolio.icon = request.POST.get('icon')
            portfolio.description = request.POST.get('description')
            portfolio.technologies = request.POST.get('technologies')
            portfolio.project_url = request.POST.get('project_url')
            portfolio.is_featured = request.POST.get('is_featured') == 'on'
            portfolio.order = request.POST.get('order', 0)
            portfolio.save()
            messages.success(request, 'Portfolio item updated successfully!')
        elif 'delete_portfolio' in request.POST:
            portfolio_id = request.POST.get('portfolio_id')
            Portfolio.objects.filter(id=portfolio_id).delete()
            messages.success(request, 'Portfolio item deleted successfully!')
        return redirect('dashboard_portfolio')
    
    return render(request, 'dashboard/portfolio.html', {'portfolio_items': portfolio_items})

# Testimonials Management
@login_required
@user_passes_test(admin_required)
def dashboard_testimonials(request):
    testimonials = Testimonial.objects.all().order_by('order')
    
    if request.method == 'POST':
        if 'add_testimonial' in request.POST:
            Testimonial.objects.create(
                name=request.POST.get('name'),
                role=request.POST.get('role'),
                company=request.POST.get('company'),
                content=request.POST.get('content'),
                avatar_initial=request.POST.get('avatar_initial'),
                rating=int(request.POST.get('rating', 5)),
                is_active=request.POST.get('is_active') == 'on',
                order=request.POST.get('order', 0)
            )
            messages.success(request, 'Testimonial added successfully!')
        elif 'edit_testimonial' in request.POST:
            testimonial_id = request.POST.get('testimonial_id')
            testimonial = get_object_or_404(Testimonial, id=testimonial_id)
            testimonial.name = request.POST.get('name')
            testimonial.role = request.POST.get('role')
            testimonial.company = request.POST.get('company')
            testimonial.content = request.POST.get('content')
            testimonial.avatar_initial = request.POST.get('avatar_initial')
            testimonial.rating = int(request.POST.get('rating', 5))
            testimonial.is_active = request.POST.get('is_active') == 'on'
            testimonial.order = request.POST.get('order', 0)
            testimonial.save()
            messages.success(request, 'Testimonial updated successfully!')
        elif 'delete_testimonial' in request.POST:
            testimonial_id = request.POST.get('testimonial_id')
            Testimonial.objects.filter(id=testimonial_id).delete()
            messages.success(request, 'Testimonial deleted successfully!')
        return redirect('dashboard_testimonials')
    
    return render(request, 'dashboard/testimonials.html', {'testimonials': testimonials})

# Messages Management
@login_required
@user_passes_test(admin_required)
def dashboard_messages(request):
    messages_list = ContactMessage.objects.all().order_by('-created_at')
    
    if request.method == 'POST':
        message_id = request.POST.get('message_id')
        message = get_object_or_404(ContactMessage, id=message_id)
        message.is_read = True
        message.save()
        messages.success(request, 'Message marked as read!')
        return redirect('dashboard_messages')
    
    return render(request, 'dashboard/messages.html', {'messages': messages_list})

# Subscribers Management
@login_required
@user_passes_test(admin_required)
def dashboard_subscribers(request):
    subscribers = NewsletterSubscriber.objects.all().order_by('-subscribed_at')
    
    if request.method == 'POST':
        subscriber_id = request.POST.get('subscriber_id')
        subscriber = get_object_or_404(NewsletterSubscriber, id=subscriber_id)
        subscriber.is_active = False
        subscriber.save()
        messages.success(request, 'Subscriber removed!')
        return redirect('dashboard_subscribers')
    
    return render(request, 'dashboard/subscribers.html', {'subscribers': subscribers})

# Settings Management
@login_required
@user_passes_test(admin_required)
def dashboard_settings(request):
    site_settings = SiteSetting.objects.first()
    if not site_settings:
        site_settings = SiteSetting.objects.create()
    
    if request.method == 'POST':
        site_settings.site_name = request.POST.get('site_name')
        site_settings.email = request.POST.get('email')
        site_settings.phone = request.POST.get('phone')
        site_settings.address = request.POST.get('address')
        site_settings.facebook = request.POST.get('facebook')
        site_settings.twitter = request.POST.get('twitter')
        site_settings.linkedin = request.POST.get('linkedin')
        site_settings.instagram = request.POST.get('instagram')
        site_settings.github = request.POST.get('github')
        
        if request.FILES.get('site_logo'):
            site_settings.site_logo = request.FILES['site_logo']
        if request.FILES.get('site_favicon'):
            site_settings.site_favicon = request.FILES['site_favicon']
        
        site_settings.save()
        messages.success(request, 'Settings updated successfully!')
        return redirect('dashboard_settings')
    
    return render(request, 'dashboard/settings.html', {'settings': site_settings})