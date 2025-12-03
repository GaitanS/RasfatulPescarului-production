#!/usr/bin/env python3
"""
Quick script to import lakes data
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake, County, FishSpecies, Facility
from django.contrib.auth.models import User
import json
from decimal import Decimal

def quick_import():
    """Quick import of lakes data"""
    print("🚀 Quick Import Lakes Data")
    print("=" * 40)
    
    # Check current data
    current_lakes = Lake.objects.count()
    print(f"📊 Current lakes in database: {current_lakes}")

    if current_lakes > 100:
        print("✅ Database already has sufficient lakes data!")
        print("🔄 To re-import, delete existing lakes first.")
        return
    
    # Load JSON data
    if not os.path.exists('lakes_export.json'):
        print("❌ lakes_export.json not found!")
        return
    
    with open('lakes_export.json', 'r', encoding='utf-8') as f:
        lakes_data = json.load(f)
    
    print(f"📁 Found {len(lakes_data)} lakes in export file")
    
    # Get admin user
    try:
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            admin_user = User.objects.create_user(
                username='admin',
                email='admin@rasfatul-pescarului.ro',
                password='admin123',
                is_superuser=True,
                is_staff=True
            )
            print("✅ Created admin user")
    except Exception as e:
        print(f"❌ Error with admin user: {e}")
        return
    
    # Import ALL lakes
    imported = 0
    errors = 0
    for i, lake_data in enumerate(lakes_data, 1):
        try:
            # Check if exists
            if Lake.objects.filter(slug=lake_data['slug']).exists():
                continue
            
            # Get county
            try:
                county = County.objects.get(slug=lake_data['county_slug'])
            except County.DoesNotExist:
                # Create county if doesn't exist
                county = County.objects.create(
                    name=lake_data['county_name'],
                    slug=lake_data['county_slug'],
                    region='TRANSILVANIA'  # Default region
                )
                print(f"✅ Created county: {county.name}")
            
            # Convert prices
            price_per_day = Decimal(str(lake_data['price_per_day'])) if lake_data['price_per_day'] else Decimal('30.00')
            price_12h = price_per_day * Decimal('0.6')
            price_24h = price_per_day
            
            # Create lake
            lake = Lake.objects.create(
                name=lake_data['name'],
                slug=lake_data['slug'],
                description=lake_data['description'] or f"Lac de pescuit în {lake_data['address']}",
                address=lake_data['address'],
                county=county,
                latitude=Decimal(str(lake_data['latitude'])) if lake_data['latitude'] else Decimal('45.9432'),
                longitude=Decimal(str(lake_data['longitude'])) if lake_data['longitude'] else Decimal('24.9668'),
                lake_type=lake_data.get('lake_type', 'private'),
                price_12h=price_12h,
                price_24h=price_24h,
                rules=lake_data.get('rules', 'Regulament standard de pescuit.'),
                contact_phone=lake_data.get('contact_phone', ''),
                contact_email=lake_data.get('contact_email', ''),
                is_active=lake_data.get('is_active', True),
                owner=admin_user
            )
            
            # Add fish species
            for species_name in lake_data.get('fish_species', []):
                species, created = FishSpecies.objects.get_or_create(
                    name=species_name,
                    defaults={'description': f'Specia {species_name}'}
                )
                lake.fish_species.add(species)
            
            # Add facilities
            for facility_name in lake_data.get('facilities', []):
                facility, created = Facility.objects.get_or_create(
                    name=facility_name,
                    defaults={
                        'description': f'Facilitate {facility_name}',
                        'icon_class': 'fas fa-check'
                    }
                )
                lake.facilities.add(facility)
            
            imported += 1
            if imported % 50 == 0:
                print(f"✅ Imported {imported} lakes so far...")

        except Exception as e:
            errors += 1
            print(f"❌ Error importing {lake_data['name']}: {e}")

    print(f"\n🎉 Import complete!")
    print(f"✅ Successfully imported: {imported} lakes")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total lakes in database: {Lake.objects.count()}")
    print(f"📊 Active lakes: {Lake.objects.filter(is_active=True).count()}")

if __name__ == '__main__':
    quick_import()
