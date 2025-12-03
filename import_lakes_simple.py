#!/usr/bin/env python
import os
import sys
import json
from decimal import Decimal
from datetime import datetime

# Add project to path
sys.path.insert(0, '/var/www/RasfatulPescarului-update')

# Disable Django logging before setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')

# Override logging settings
from django.conf import settings
if not settings.configured:
    settings.configure(
        DEBUG=False,
        DATABASES={
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': '/var/www/RasfatulPescarului-update/db.sqlite3',
            }
        },
        INSTALLED_APPS=[
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'main',
        ],
        SECRET_KEY='temp-key-for-import',
        USE_TZ=True,
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                },
            },
            'root': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        }
    )

import django
django.setup()

from main.models import Lake, LakePhoto, LakeReview, County, FishSpecies, Facility
from django.contrib.auth.models import User
from django.utils import timezone

def import_lakes():
    if not os.path.exists('lakes_export.json'):
        print("ERROR: lakes_export.json file not found!")
        return
    
    with open('lakes_export.json', 'r', encoding='utf-8') as f:
        lakes_data = json.load(f)
    
    print(f"Found {len(lakes_data)} lakes to import...")
    
    imported_count = 0
    error_count = 0
    
    for lake_data in lakes_data:
        try:
            # Get county
            try:
                county = County.objects.get(slug=lake_data['county_slug'])
            except County.DoesNotExist:
                print(f"WARNING: County {lake_data['county_slug']} not found")
                error_count += 1
                continue
            
            # Get owner
            try:
                owner = User.objects.get(username=lake_data['owner_username'])
            except User.DoesNotExist:
                owner = User.objects.filter(is_superuser=True).first()
                if not owner:
                    print(f"WARNING: No admin user found")
                    error_count += 1
                    continue
            
            # Create lake
            lake, created = Lake.objects.get_or_create(
                slug=lake_data['slug'],
                defaults={
                    'name': lake_data['name'],
                    'description': lake_data['description'],
                    'address': lake_data['address'],
                    'county': county,
                    'latitude': Decimal(str(lake_data['latitude'])) if lake_data['latitude'] else None,
                    'longitude': Decimal(str(lake_data['longitude'])) if lake_data['longitude'] else None,
                    'lake_type': lake_data.get('lake_type', ''),
                    'price_per_day': Decimal(str(lake_data['price_per_day'])) if lake_data['price_per_day'] else None,
                    'rules': lake_data.get('rules', ''),
                    'is_active': lake_data.get('is_active', True),
                    'owner': owner,
                }
            )
            
            if created:
                imported_count += 1
                print(f"✅ Created: {lake.name}")
            
        except Exception as e:
            print(f"❌ Error: {lake_data.get('name', 'Unknown')}: {e}")
            error_count += 1
    
    print(f"\n🎉 Import completed!")
    print(f"✅ Imported: {imported_count} lakes")
    print(f"❌ Errors: {error_count} lakes")

if __name__ == '__main__':
    import_lakes()
