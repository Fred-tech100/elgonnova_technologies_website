#!/usr/bin/env python
import os
import sys
import django

print("=== Starting superuser creation script ===")

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elgonnova.settings')

try:
    django.setup()
    print("Django setup successful")
except Exception as e:
    print(f"Error setting up Django: {e}")
    sys.exit(1)

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'mangara'
password = 'Deus@0956'

print(f"Checking if user '{username}' exists...")

try:
    user_exists = User.objects.filter(username=username).exists()
    print(f"User exists: {user_exists}")
    
    if not user_exists:
        print("Creating superuser...")
        # Try both methods
        try:
            User.objects.create_superuser(username, None, password)
            print(f"✅ Superuser '{username}' created successfully!")
        except TypeError:
            User.objects.create_superuser(username, password)
            print(f"✅ Superuser '{username}' created successfully!")
    else:
        print(f"ℹ️ Superuser '{username}' already exists")
        
    # Verify the user has admin permissions
    user = User.objects.get(username=username)
    print(f"is_superuser: {user.is_superuser}")
    print(f"is_staff: {user.is_staff}")
    print(f"is_active: {user.is_active}")
    
    if not user.is_superuser or not user.is_staff:
        print("Fixing permissions...")
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save()
        print("Permissions fixed!")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("=== Superuser script finished ===")