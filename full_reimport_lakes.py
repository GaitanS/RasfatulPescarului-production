#!/usr/bin/env python3
"""
Full re-import of all lakes data
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

def full_reimport():
    """Full re-import of all lakes"""
    print("🔄 FULL RE-IMPORT OF LAKES DATA")
    print("=" * 50)
    
    # Show current stats
    current_lakes = Lake.objects.count()
    print(f"📊 Current lakes: {current_lakes}")
    
    # Ask for confirmation
    if current_lakes > 0:
        print("⚠️  This will DELETE all existing lakes and re-import from JSON!")
        confirm = input("Type 'YES' to continue: ")
        if confirm != 'YES':
            print("❌ Import cancelled.")
            return
    
    # Delete existing lakes
    if current_lakes > 0:
        print("🗑️  Deleting existing lakes...")
        Lake.objects.all().delete()
        print(f"✅ Deleted {current_lakes} lakes")
    
    # Load JSON data
    if not os.path.exists('lakes_export.json'):
        print("❌ lakes_export.json not found!")
        return
    
    with open('lakes_export.json', 'r', encoding='utf-8') as f:
        lakes_data = json.load(f)
    
    print(f"📁 Found {len(lakes_data)} lakes in export file")
    
    # Get or create admin user
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
    skipped = 0
    
    print("🚀 Starting import...")
    
    for i, lake_data in enumerate(lakes_data, 1):
        try:
            # Check if exists (shouldn't after deletion, but just in case)
            if Lake.objects.filter(slug=lake_data['slug']).exists():
                skipped += 1
                continue
            
            # Get or create county
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
            price_per_day = lake_data.get('price_per_day', 30.0)
            if price_per_day:
                price_per_day = Decimal(str(price_per_day))
            else:
                price_per_day = Decimal('30.00')
            
            price_12h = price_per_day * Decimal('0.6')  # 60% for 12h
            price_24h = price_per_day  # Full price for 24h
            
            # Create lake
            lake = Lake.objects.create(
                name=lake_data['name'],
                slug=lake_data['slug'],
                description=lake_data.get('description', '') or f"Lac de pescuit în {lake_data['address']}",
                address=lake_data['address'],
                county=county,
                latitude=Decimal(str(lake_data['latitude'])) if lake_data.get('latitude') else Decimal('45.9432'),
                longitude=Decimal(str(lake_data['longitude'])) if lake_data.get('longitude') else Decimal('24.9668'),
                lake_type=lake_data.get('lake_type', 'private'),
                price_12h=price_12h,
                price_24h=price_24h,
                rules=lake_data.get('rules', '') or 'Regulament standard de pescuit.',
                contact_phone=lake_data.get('contact_phone', ''),
                contact_email=lake_data.get('contact_email', ''),
                is_active=lake_data.get('is_active', True),
                owner=admin_user
            )
            
            # Add fish species
            for species_name in lake_data.get('fish_species', []):
                if species_name:  # Skip empty names
                    species, created = FishSpecies.objects.get_or_create(
                        name=species_name,
                        defaults={'category': 'other'}  # Default category
                    )
                    lake.fish_species.add(species)
            
            # Add facilities
            for facility_name in lake_data.get('facilities', []):
                if facility_name:  # Skip empty names
                    facility, created = Facility.objects.get_or_create(
                        name=facility_name,
                        defaults={'icon_class': 'fas fa-check'}
                    )
                    lake.facilities.add(facility)
            
            imported += 1
            
            # Progress indicator
            if imported % 100 == 0:
                print(f"✅ Imported {imported} lakes so far...")
            
        except Exception as e:
            errors += 1
            print(f"❌ Error importing {lake_data.get('name', 'Unknown')}: {e}")
            if errors > 50:  # Stop if too many errors
                print("❌ Too many errors, stopping import.")
                break
    
    print(f"\n🎉 IMPORT COMPLETE!")
    print(f"✅ Successfully imported: {imported} lakes")
    print(f"⏭️  Skipped: {skipped} lakes")
    print(f"❌ Errors: {errors}")
    print(f"📊 Total lakes in database: {Lake.objects.count()}")
    print(f"📊 Active lakes: {Lake.objects.filter(is_active=True).count()}")
    print(f"📊 Counties: {County.objects.count()}")
    print(f"📊 Fish species: {FishSpecies.objects.count()}")
    print(f"📊 Facilities: {Facility.objects.count()}")

if __name__ == '__main__':
    full_reimport()
