from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, default='ElgonNova Technologies')
    site_logo = models.ImageField(upload_to='settings/', blank=True, null=True)
    site_favicon = models.ImageField(upload_to='settings/', blank=True, null=True)
    email = models.EmailField(default='elgonnnovatechnologies@gmail.com')
    phone = models.CharField(max_length=20, default='+256 753 0825 829')
    address = models.TextField(default='Mbale City, Uganda')
    facebook = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    github = models.URLField(blank=True)
    
    def __str__(self):
        return self.site_name
    
    class Meta:
        verbose_name = 'Site Setting'

class Service(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, help_text='FontAwesome icon class (e.g., fas fa-laptop-code)')
    description = models.TextField()
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']

class PortfolioCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name

class Portfolio(models.Model):
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('software', 'Software'),
        ('iot', 'IoT'),
        ('data', 'Data & AI'),
    ]
    
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=10, help_text='Emoji or icon (e.g., 🛒)')
    description = models.TextField()
    technologies = models.CharField(max_length=200)
    image = models.ImageField(upload_to='portfolio/', blank=True, null=True)
    project_url = models.URLField(blank=True)
    is_featured = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Portfolio'

class BlogPost(models.Model):
    CATEGORY_CHOICES = [
        ('AI & ML', 'AI & Machine Learning'),
        ('IoT', 'Internet of Things'),
        ('Business', 'Business & Digital Transformation'),
        ('Tech News', 'Technology News'),
    ]
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    excerpt = models.TextField()
    content = models.TextField()
    featured_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    icon = models.CharField(max_length=10, help_text='Emoji for thumbnail (e.g., 🤖)')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    content = models.TextField()
    avatar_initial = models.CharField(max_length=2, help_text='Two letters for avatar')
    rating = models.IntegerField(default=5)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.company}"
    
    class Meta:
        ordering = ['order']

class ContactMessage(models.Model):
    SERVICE_CHOICES = [
        ('Software Development', 'Software Development'),
        ('Website Development', 'Website Development'),
        ('IoT Solutions', 'IoT Solutions'),
        ('Computer Repair & Maintenance', 'Computer Repair & Maintenance'),
        ('ICT Consultancy', 'ICT Consultancy'),
        ('Data Analysis & ML', 'Data Analysis & ML'),
        ('Graphics Designing', 'Graphics Designing'),
    ]
    
    BUDGET_CHOICES = [
        ('Under UGX 1.8M', 'Under UGX 1.8M'),
        ('UGX 1.8M – UGX 2M', 'UGX 1.8M – UGX 2M'),
        ('UGX 2M – UGX 10M', 'UGX 2M – UGX 10M'),
        ('UGX 10M+', 'UGX 10M+'),
    ]
    
    name = models.CharField(max_length=100)
    email = models.EmailField()
    service = models.CharField(max_length=100, choices=SERVICE_CHOICES)
    budget = models.CharField(max_length=50, choices=BUDGET_CHOICES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.name}"
    
    class Meta:
        ordering = ['-created_at']

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email

class Statistic(models.Model):
    label = models.CharField(max_length=100)
    value = models.IntegerField()
    suffix = models.CharField(max_length=10, blank=True, help_text='e.g., +, %, etc.')
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.label}: {self.value}{self.suffix}"
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = 'Statistics'
# Add to core/models.py after existing models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    quote = models.TextField(blank=True, help_text="Personal quote or message from team member")
    image = models.ImageField(upload_to='team/', blank=True, null=True)
    avatar_initial = models.CharField(max_length=2, help_text="Two letters for avatar")
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    social_linkedin = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True)
    social_github = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['order']
        verbose_name_plural = "Team Members"

class Career(models.Model):
    JOB_TYPE_CHOICES = [
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Remote', 'Remote'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('Entry Level', 'Entry Level (0-2 years)'),
        ('Mid Level', 'Mid Level (3-5 years)'),
        ('Senior Level', 'Senior Level (5+ years)'),
        ('Lead/Manager', 'Lead/Manager'),
    ]
    
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=50, choices=EXPERIENCE_CHOICES)
    location = models.CharField(max_length=100)
    salary_range = models.CharField(max_length=100, blank=True, help_text="e.g., $30k - $50k")
    description = models.TextField()
    requirements = models.TextField(help_text="List requirements, one per line or bullet points")
    responsibilities = models.TextField(help_text="List responsibilities, one per line or bullet points")
    benefits = models.TextField(blank=True, help_text="List benefits, one per line or bullet points")
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    application_deadline = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Careers"

class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('interviewed', 'Interviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    career = models.ForeignKey(Career, on_delete=models.CASCADE, related_name='applications')
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    portfolio_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    cover_letter = models.TextField()
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.full_name} - {self.career.title}"
    
    class Meta:
        ordering = ['-applied_at']

class CEOMessage(models.Model):
    name = models.CharField(max_length=100, default="CEO")
    title = models.CharField(max_length=100, default="Chief Executive Officer")
    message = models.TextField()
    quote = models.CharField(max_length=200, blank=True, help_text="Inspirational quote")
    image = models.ImageField(upload_to='ceo/', blank=True, null=True)
    avatar_initial = models.CharField(max_length=2, default="CE")
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Message from {self.name}"
    
    class Meta:
        verbose_name = "CEO Message"
        verbose_name_plural = "CEO Messages"