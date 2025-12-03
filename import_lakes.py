#!/usr/bin/env python
import os
import sys
import django
import json
from decimal import Decimal
from datetime import datetime

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake, LakePhoto, LakeReview, County, FishSpecies, Facility
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files.base import ContentFile

def import_lakes():
    """Import lakes from JSON file"""
    
    if not os.path.exists('lakes_export.json'):
        print("ERROR: lakes_export.json file not found!")
        return
    
    with open('lakes_export.json', 'r', encoding='utf-8') as f:
        lakes_data = json.load(f)
    
    print(f"Starting import of {len(lakes_data)} lakes...")
    
    imported_count = 0
    skipped_count = 0
    error_count = 0
    
    for lake_data in lakes_data:
        try:
            # Check if lake already exists by slug
            if Lake.objects.filter(slug=lake_data['slug']).exists():
                print(f"SKIPPED: Lake '{lake_data['name']}' already exists (slug: {lake_data['slug']})")
                skipped_count += 1
                continue
            
            # Get or create county
            try:
                county = County.objects.get(slug=lake_data['county_slug'])
            except County.DoesNotExist:
                print(f"ERROR: County '{lake_data['county_name']}' not found for lake '{lake_data['name']}'")
                error_count += 1
                continue
            
            # Get or create owner (use admin if original owner doesn't exist)
            try:
                owner = User.objects.get(username=lake_data['owner_username'])
            except User.DoesNotExist:
                owner = User.objects.filter(is_superuser=True).first()
                if not owner:
                    print(f"ERROR: No admin user found for lake '{lake_data['name']}'")
                    error_count += 1
                    continue
            
            # Convert price_per_day to price_12h and price_24h
            price_per_day = Decimal(str(lake_data['price_per_day'])) if lake_data['price_per_day'] else Decimal('30.00')
            price_12h = price_per_day * Decimal('0.6')  # 60% of daily price for 12h
            price_24h = price_per_day  # Full daily price for 24h

            # Create lake
            lake = Lake.objects.create(
                name=lake_data['name'],
                slug=lake_data['slug'],
                description=lake_data['description'],
                address=lake_data['address'],
                county=county,
                latitude=Decimal(str(lake_data['latitude'])) if lake_data['latitude'] else None,
                longitude=Decimal(str(lake_data['longitude'])) if lake_data['longitude'] else None,
                google_maps_embed=lake_data['google_maps_embed'],
                lake_type=lake_data['lake_type'],
                price_12h=price_12h,
                price_24h=price_24h,
                rules=lake_data['rules'],
                contact_phone=lake_data['contact_phone'],
                contact_email=lake_data['contact_email'],
                number_of_stands=lake_data['number_of_stands'],
                surface_area=Decimal(str(lake_data['surface_area'])) if lake_data['surface_area'] else None,
                depth_min=Decimal(str(lake_data['depth_min'])) if lake_data['depth_min'] else None,
                depth_max=Decimal(str(lake_data['depth_max'])) if lake_data['depth_max'] else None,
                is_active=lake_data['is_active'],
                owner=owner,
                created_at=timezone.datetime.fromisoformat(lake_data['created_at'].replace('Z', '+00:00')),
                updated_at=timezone.datetime.fromisoformat(lake_data['updated_at'].replace('Z', '+00:00'))
            )
            
            # Add optional fields if they exist
            if lake_data.get('depth_average'):
                lake.depth_average = Decimal(str(lake_data['depth_average']))
            if lake_data.get('length_min'):
                lake.length_min = Decimal(str(lake_data['length_min']))
            if lake_data.get('length_max'):
                lake.length_max = Decimal(str(lake_data['length_max']))
            if lake_data.get('width_min'):
                lake.width_min = Decimal(str(lake_data['width_min']))
            if lake_data.get('width_max'):
                lake.width_max = Decimal(str(lake_data['width_max']))
            if lake_data.get('website'):
                lake.website = lake_data['website']
            if lake_data.get('facebook_url'):
                lake.facebook_url = lake_data['facebook_url']
            if lake_data.get('instagram_url'):
                lake.instagram_url = lake_data['instagram_url']
            
            lake.save()
            
            # Add fish species
            for species_name in lake_data['fish_species']:
                try:
                    species = FishSpecies.objects.get(name=species_name)
                    lake.fish_species.add(species)
                except FishSpecies.DoesNotExist:
                    print(f"WARNING: Fish species '{species_name}' not found for lake '{lake.name}'")
            
            # Add facilities
            for facility_name in lake_data['facilities']:
                try:
                    facility = Facility.objects.get(name=facility_name)
                    lake.facilities.add(facility)
                except Facility.DoesNotExist:
                    print(f"WARNING: Facility '{facility_name}' not found for lake '{lake.name}'")
            
            # Import photos (skip file copying for now)
            for photo_data in lake_data['photos']:
                LakePhoto.objects.create(
                    lake=lake,
                    title=photo_data['title'],
                    description=photo_data['description'],
                    order=photo_data['order'],
                    is_main=photo_data['is_main'],
                    created_at=timezone.datetime.fromisoformat(photo_data['created_at'].replace('Z', '+00:00'))
                )
            
            # Import reviews
            for review_data in lake_data['reviews']:
                visit_date = None
                if review_data['visit_date']:
                    visit_date = timezone.datetime.fromisoformat(review_data['visit_date'].replace('Z', '+00:00')).date()
                
                LakeReview.objects.create(
                    lake=lake,
                    reviewer_name=review_data['reviewer_name'],
                    reviewer_email=review_data['reviewer_email'],
                    rating=review_data['rating'],
                    title=review_data['title'],
                    comment=review_data['comment'],
                    visit_date=visit_date,
                    is_approved=review_data['is_approved'],
                    is_spam=review_data['is_spam'],
                    ip_address=review_data['ip_address'],
                    created_at=timezone.datetime.fromisoformat(review_data['created_at'].replace('Z', '+00:00')),
                    updated_at=timezone.datetime.fromisoformat(review_data['updated_at'].replace('Z', '+00:00'))
                )
            
            print(f"IMPORTED: {lake.name} (ID: {lake.id})")
            imported_count += 1
            
        except Exception as e:
            print(f"ERROR importing lake '{lake_data['name']}': {str(e)}")
            error_count += 1
    
    print(f"\n=== IMPORT SUMMARY ===")
    print(f"Imported: {imported_count}")
    print(f"Skipped: {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Total processed: {imported_count + skipped_count + error_count}")

if __name__ == "__main__":
    import_lakes()
