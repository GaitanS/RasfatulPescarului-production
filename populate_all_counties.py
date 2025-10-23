#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Populate All 42 Romanian Counties (41 Counties + București)
Adds all counties to the database with correct names and slugs
"""

import os
import sys
import django

# Fix encoding for Windows console
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import County

# Complete list of all 42 Romanian counties (41 + București)
ALL_COUNTIES = [
    {'slug': 'alba', 'name': 'Alba'},
    {'slug': 'arad', 'name': 'Arad'},
    {'slug': 'arges', 'name': 'Argeș'},
    {'slug': 'bacau', 'name': 'Bacău'},
    {'slug': 'bihor', 'name': 'Bihor'},
    {'slug': 'bistrita-nasaud', 'name': 'Bistrița-Năsăud'},
    {'slug': 'botosani', 'name': 'Botoșani'},
    {'slug': 'braila', 'name': 'Brăila'},
    {'slug': 'brasov', 'name': 'Brașov'},
    {'slug': 'bucuresti', 'name': 'București'},
    {'slug': 'buzau', 'name': 'Buzău'},
    {'slug': 'caras-severin', 'name': 'Caraș-Severin'},
    {'slug': 'calarasi', 'name': 'Călărași'},
    {'slug': 'cluj', 'name': 'Cluj'},
    {'slug': 'constanta', 'name': 'Constanța'},
    {'slug': 'covasna', 'name': 'Covasna'},
    {'slug': 'dambovita', 'name': 'Dâmbovița'},
    {'slug': 'dolj', 'name': 'Dolj'},
    {'slug': 'galati', 'name': 'Galați'},
    {'slug': 'giurgiu', 'name': 'Giurgiu'},
    {'slug': 'gorj', 'name': 'Gorj'},
    {'slug': 'harghita', 'name': 'Harghita'},
    {'slug': 'hunedoara', 'name': 'Hunedoara'},
    {'slug': 'ialomita', 'name': 'Ialomița'},
    {'slug': 'iasi', 'name': 'Iași'},
    {'slug': 'ilfov', 'name': 'Ilfov'},
    {'slug': 'maramures', 'name': 'Maramureș'},
    {'slug': 'mehedinti', 'name': 'Mehedinți'},
    {'slug': 'mures', 'name': 'Mureș'},
    {'slug': 'neamt', 'name': 'Neamț'},
    {'slug': 'olt', 'name': 'Olt'},
    {'slug': 'prahova', 'name': 'Prahova'},
    {'slug': 'salaj', 'name': 'Sălaj'},
    {'slug': 'satu-mare', 'name': 'Satu Mare'},
    {'slug': 'sibiu', 'name': 'Sibiu'},
    {'slug': 'suceava', 'name': 'Suceava'},
    {'slug': 'teleorman', 'name': 'Teleorman'},
    {'slug': 'timis', 'name': 'Timiș'},
    {'slug': 'tulcea', 'name': 'Tulcea'},
    {'slug': 'valcea', 'name': 'Vâlcea'},
    {'slug': 'vaslui', 'name': 'Vaslui'},
    {'slug': 'vrancea', 'name': 'Vrancea'},
]

def populate_all_counties():
    """Add all 42 Romanian counties to the database"""
    print("Populare Toate Judetele Romaniei (42 total)\n")
    print("=" * 70)

    created_count = 0
    existing_count = 0

    for county_data in ALL_COUNTIES:
        county, created = County.objects.get_or_create(
            slug=county_data['slug'],
            defaults={'name': county_data['name']}
        )

        if created:
            print(f"   [+] Creat: {county.name} ({county.slug})")
            created_count += 1
        else:
            print(f"   [=] Exista: {county.name} ({county.slug})")
            existing_count += 1

    print("\n" + "=" * 70)
    print(f"\nRezumat:")
    print(f"   Judete noi create: {created_count}")
    print(f"   Judete existente: {existing_count}")
    print(f"   Total judete in DB: {County.objects.count()}")
    print(f"\nPopulare completata cu succes!")

    # List counties without guides
    counties_without_guides = County.objects.filter(
        guide_content__isnull=True
    ).order_by('name')

    print(f"\n\nJudete fara ghiduri de pescuit ({counties_without_guides.count()}):")
    for county in counties_without_guides:
        print(f"   - {county.name}")

if __name__ == '__main__':
    populate_all_counties()
