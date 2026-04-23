from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Service, Portfolio, BlogPost, TeamMember, Testimonial, Statistic, SiteSetting, TeamMember, Career, JobApplication, CEOMessage, SiteSetting
from .forms import ContactForm, NewsletterForm
from django.core.mail import send_mail
from django.conf import settings

def home(request):
    services = Service.objects.filter(is_active=True)
    portfolio_items = Portfolio.objects.all()
    blog_posts = BlogPost.objects.filter(is_published=True)[:3]
    testimonials = Testimonial.objects.filter(is_active=True)
    stats = Statistic.objects.filter(is_active=True)
    site_settings = SiteSetting.objects.first()
    team_members = TeamMember.objects.filter(is_active=True)
    careers = Career.objects.filter(is_active=True)[:3]  # Show only 3 latest on homepage
    ceo_message = CEOMessage.objects.filter(is_active=True).first()
    
    if request.method == 'POST':
        if 'contact_form' in request.POST:
            contact_form = ContactForm(request.POST)
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'Thank you! Your message has been sent.')
                return redirect('core:home')
        elif 'newsletter_form' in request.POST:
            newsletter_form = NewsletterForm(request.POST)
            if newsletter_form.is_valid():
                newsletter_form.save()
                messages.success(request, 'Subscribed! Welcome to the ElgonNova community.')
                return redirect('core:home')
    
    contact_form = ContactForm()
    newsletter_form = NewsletterForm()
    
    context = {
        'services': services,
        'portfolio_items': portfolio_items,
        'blog_posts': blog_posts,
        'testimonials': testimonials,
        'stats': stats,
        'site_settings': site_settings,
        'contact_form': contact_form,
        'newsletter_form': newsletter_form,
        'team_members': team_members,
        'careers': careers,
        'ceo_message': ceo_message,
    }
    return render(request, 'index.html', context)

def blog_detail(request, slug):
    post = BlogPost.objects.get(slug=slug, is_published=True)
    post.views += 1
    post.save()
    return render(request, 'blog_detail.html', {'post': post})

def portfolio_detail(request, id):
    portfolio = Portfolio.objects.get(id=id)
    return render(request, 'portfolio_detail.html', {'portfolio': portfolio})
def careers_list(request):
    careers = Career.objects.filter(is_active=True)
    return render(request, 'careers.html', {'careers': careers})

def career_detail(request, slug):
    career = Career.objects.get(slug=slug, is_active=True)
    return render(request, 'career_detail.html', {'career': career})

def apply_job(request, slug):
    career = Career.objects.get(slug=slug, is_active=True)
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        portfolio_url = request.POST.get('portfolio_url')
        linkedin_url = request.POST.get('linkedin_url')
        cover_letter = request.POST.get('cover_letter')
        resume = request.FILES.get('resume')
        
        application = JobApplication.objects.create(
            career=career,
            full_name=full_name,
            email=email,
            phone=phone,
            portfolio_url=portfolio_url,
            linkedin_url=linkedin_url,
            cover_letter=cover_letter,
            resume=resume
        )
        
        # Optional: Send email notification
        send_mail(
            f'New Job Application: {career.title}',
            f'New application from {full_name} for {career.title}',
            settings.DEFAULT_FROM_EMAIL,
            [settings.ADMIN_EMAIL],
            fail_silently=True,
        )
        
        messages.success(request, 'Application submitted successfully! We will contact you soon.')
        return redirect('core:careers')
    
    return render(request, 'apply_job.html', {'career': career})

def team_members(request):
    team_members = TeamMember.objects.filter(is_active=True)
    return render(request, 'team.html', {'team_members': team_members})
