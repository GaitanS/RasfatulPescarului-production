#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to import lakes data from lakes_export.json backup file
This will restore all 203 lakes with their counties, fish species, and facilities
"""
import os
import sys
import json
import django
from decimal import Decimal
from datetime import datetime

# Fix pentru encoding Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils import timezone
from main.models import County, FishSpecies, Facility, Lake

def get_region_for_county(county_name):
    """Map county names to regions"""
    region_map = {
        # Moldova
        'Bacău': 'MOLDOVA', 'Botoșani': 'MOLDOVA', 'Galați': 'MOLDOVA',
        'Iași': 'MOLDOVA', 'Neamț': 'MOLDOVA', 'Suceava': 'MOLDOVA', 'Vaslui': 'MOLDOVA', 'Vrancea': 'MOLDOVA',
        # Muntenia
        'Argeș': 'MUNTENIA', 'Buzău': 'MUNTENIA', 'Călărași': 'MUNTENIA', 'Dâmbovița': 'MUNTENIA',
        'Giurgiu': 'MUNTENIA', 'Ialomița': 'MUNTENIA', 'Prahova': 'MUNTENIA', 'Teleorman': 'MUNTENIA',
        # Oltenia
        'Dolj': 'OLTENIA', 'Gorj': 'OLTENIA', 'Mehedinți': 'OLTENIA', 'Olt': 'OLTENIA', 'Vâlcea': 'OLTENIA',
        # Banat
        'Caraș-Severin': 'BANAT', 'Timiș': 'BANAT',
        # Crișana
        'Arad': 'CRISANA', 'Bihor': 'CRISANA',
        # Maramureș
        'Maramureș': 'MARAMURES', 'Satu Mare': 'MARAMURES',
        # Transilvania
        'Alba': 'TRANSILVANIA', 'Bistrița-Năsăud': 'TRANSILVANIA', 'Brașov': 'TRANSILVANIA',
        'Cluj': 'TRANSILVANIA', 'Covasna': 'TRANSILVANIA', 'Harghita': 'TRANSILVANIA',
        'Hunedoara': 'TRANSILVANIA', 'Mureș': 'TRANSILVANIA', 'Sălaj': 'TRANSILVANIA', 'Sibiu': 'TRANSILVANIA',
        # Dobrogea
        'Constanța': 'DOBROGEA', 'Tulcea': 'DOBROGEA',
        # București
        'București': 'BUCURESTI', 'Ilfov': 'BUCURESTI'
    }
    return region_map.get(county_name, 'TRANSILVANIA')  # Default to Transilvania

def import_data():
    """Main import function"""
    print("=" * 80)
    print("IMPORT LACURI DIN BACKUP")
    print("=" * 80)
    print()

    # Load JSON data
    print("[1/5] Citesc fișierul lakes_export.json...")
    with open('lakes_export.json', 'r', encoding='utf-8') as f:
        lakes_data = json.load(f)
    print(f"✓ Am găsit {len(lakes_data)} lacuri în backup\n")

    # Get admin user
    print("[2/5] Verific utilizatorul admin...")
    admin_user = User.objects.filter(username='admin').first()
    if not admin_user:
        print("✗ Nu există utilizator 'admin'! Îl creez...")
        admin_user = User.objects.create_user(
            username='admin',
            email='admin@rasfatulpescarului.ro',
            password='admin123',
            is_staff=True,
            is_superuser=True
        )
        print("✓ Utilizator admin creat\n")
    else:
        print(f"✓ Utilizator admin găsit (ID: {admin_user.id})\n")

    # Extract unique counties
    print("[3/5] Creez județele...")
    unique_counties = {}
    for lake in lakes_data:
        county_name = lake['county_name']
        county_slug = lake['county_slug']
        if county_slug not in unique_counties:
            unique_counties[county_slug] = county_name

    counties_map = {}
    for slug, name in unique_counties.items():
        county, created = County.objects.get_or_create(
            slug=slug,
            defaults={
                'name': name,
                'region': get_region_for_county(name)
            }
        )
        counties_map[slug] = county
        status = "✓ Creat" if created else "○ Exista"
        print(f"  {status}: {name} ({slug})")
    print(f"✓ Total: {len(counties_map)} județe\n")

    # Extract unique fish species
    print("[4/5] Creez speciile de pești...")
    unique_fish = set()
    for lake in lakes_data:
        for fish_name in lake['fish_species']:
            unique_fish.add(fish_name)

    fish_species_map = {}
    for fish_name in sorted(unique_fish):
        # Try to get existing fish by name first
        fish = FishSpecies.objects.filter(name=fish_name).first()
        if fish:
            fish_species_map[fish_name] = fish
            print(f"  ○ Exista: {fish_name}")
        else:
            # Create new fish with unique slug
            base_slug = slugify(fish_name)
            slug = base_slug
            counter = 1
            while FishSpecies.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            fish = FishSpecies.objects.create(
                name=fish_name,
                slug=slug,
                category='other',
                is_active=True
            )
            fish_species_map[fish_name] = fish
            print(f"  ✓ Creat: {fish_name}")
    print(f"✓ Total: {len(fish_species_map)} specii de pești\n")

    # Extract unique facilities
    print("[4/5] Creez facilitățile...")
    unique_facilities = set()
    for lake in lakes_data:
        for facility_name in lake['facilities']:
            unique_facilities.add(facility_name)

    # Map facility names to icon classes
    facility_icons = {
        'Parcare': 'fas fa-parking',
        'Toalete': 'fas fa-toilet',
        'Corturi': 'fas fa-campground',
        'Drum accesibil auto': 'fas fa-car',
        'Standuri numerotate': 'fas fa-hashtag',
        'Restaurant': 'fas fa-utensils',
        'Cazare': 'fas fa-bed',
        'Magazin': 'fas fa-store',
        'Electricitate': 'fas fa-bolt',
        'Apă curentă': 'fas fa-faucet',
        'Duș': 'fas fa-shower',
        'Grătar': 'fas fa-fire',
        'Wi-Fi': 'fas fa-wifi',
        'Pescuit din barcă': 'fas fa-ship',
        'Închiriere bărci': 'fas fa-ship',
        'Zonă copii': 'fas fa-child',
        'Teren sport': 'fas fa-volleyball-ball',
        'Piscină': 'fas fa-swimming-pool',
        'Bar': 'fas fa-glass-martini-alt',
        'Frigider': 'fas fa-snowflake',
        'Iluminat nocturn': 'fas fa-lightbulb',
    }

    facilities_map = {}
    for facility_name in sorted(unique_facilities):
        # Try to get existing facility by name first
        facility = Facility.objects.filter(name=facility_name).first()
        if facility:
            facilities_map[facility_name] = facility
            print(f"  ○ Exista: {facility_name}")
        else:
            facility = Facility.objects.create(
                name=facility_name,
                icon_class=facility_icons.get(facility_name, 'fas fa-check-circle'),
                category='basic',
                is_active=True
            )
            facilities_map[facility_name] = facility
            print(f"  ✓ Creat: {facility_name}")
    print(f"✓ Total: {len(facilities_map)} facilități\n")

    # Import lakes
    print("[5/5] Import lacuri...")
    print("-" * 80)

    imported_count = 0
    skipped_count = 0
    error_count = 0

    for i, lake_data in enumerate(lakes_data, 1):
        try:
            # Check if lake already exists
            existing_lake = Lake.objects.filter(slug=lake_data['slug']).first()
            if existing_lake:
                print(f"  [{i}/{len(lakes_data)}] ○ Există deja: {lake_data['name']}")
                skipped_count += 1
                continue

            # Get county
            county = counties_map.get(lake_data['county_slug'])
            if not county:
                print(f"  [{i}/{len(lakes_data)}] ✗ Județ lipsă pentru: {lake_data['name']}")
                error_count += 1
                continue

            # Create lake
            lake = Lake.objects.create(
                owner=admin_user,
                name=lake_data['name'],
                slug=lake_data['slug'],
                description=lake_data['description'] or '',
                address=lake_data['address'],
                county=county,
                latitude=Decimal(str(lake_data['latitude'])),
                longitude=Decimal(str(lake_data['longitude'])),
                google_maps_embed=lake_data.get('google_maps_embed') or None,
                lake_type=lake_data.get('lake_type', 'private'),
                price_12h=Decimal(str(lake_data['price_per_day'])),  # Use same price for both
                price_24h=Decimal(str(lake_data['price_per_day'])),
                rules=lake_data.get('rules', ''),
                contact_phone=lake_data['contact_phone'],
                contact_email=lake_data['contact_email'],
                number_of_stands=lake_data.get('number_of_stands'),
                surface_area=Decimal(str(lake_data['surface_area'])) if lake_data.get('surface_area') else None,
                depth_min=Decimal(str(lake_data['depth_min'])) if lake_data.get('depth_min') else None,
                depth_max=Decimal(str(lake_data['depth_max'])) if lake_data.get('depth_max') else None,
                depth_average=Decimal(str(lake_data['depth_average'])) if lake_data.get('depth_average') else None,
                length_min=Decimal(str(lake_data['length_min'])) if lake_data.get('length_min') else None,
                length_max=Decimal(str(lake_data['length_max'])) if lake_data.get('length_max') else None,
                width_min=Decimal(str(lake_data['width_min'])) if lake_data.get('width_min') else None,
                width_max=Decimal(str(lake_data['width_max'])) if lake_data.get('width_max') else None,
                website=lake_data.get('website', ''),
                facebook_url=lake_data.get('facebook_url', ''),
                instagram_url=lake_data.get('instagram_url', ''),
                is_active=lake_data.get('is_active', True),
            )

            # Add fish species
            for fish_name in lake_data['fish_species']:
                fish = fish_species_map.get(fish_name)
                if fish:
                    lake.fish_species.add(fish)

            # Add facilities
            for facility_name in lake_data['facilities']:
                facility = facilities_map.get(facility_name)
                if facility:
                    lake.facilities.add(facility)

            print(f"  [{i}/{len(lakes_data)}] ✓ Importat: {lake_data['name']} ({lake_data['county_name']})")
            imported_count += 1

        except Exception as e:
            print(f"  [{i}/{len(lakes_data)}] ✗ Eroare la {lake_data['name']}: {str(e)}")
            error_count += 1

    print("-" * 80)
    print()

    # Final statistics
    print("=" * 80)
    print("STATISTICI FINALE")
    print("=" * 80)
    print(f"✓ Lacuri importate:  {imported_count}")
    print(f"○ Lacuri existente:  {skipped_count}")
    print(f"✗ Erori:             {error_count}")
    print(f"─ Total procesate:   {len(lakes_data)}")
    print()
    print(f"✓ Județe în baza de date:     {County.objects.count()}")
    print(f"✓ Specii în baza de date:     {FishSpecies.objects.count()}")
    print(f"✓ Facilități în baza de date: {Facility.objects.count()}")
    print(f"✓ Lacuri în baza de date:     {Lake.objects.count()}")
    print(f"✓ Lacuri active:              {Lake.objects.filter(is_active=True).count()}")
    print("=" * 80)
    print()
    print("Import finalizat cu succes!")
    print("Acum poți vizita: http://127.0.0.1:8000/locations/map/")
    print()

if __name__ == '__main__':
    import_data()
