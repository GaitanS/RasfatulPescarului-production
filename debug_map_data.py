#!/usr/bin/env python3
"""
Script pentru debug-ul datelor de pe hartă
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake, County
import json

def debug_map_data():
    """Debug datele pentru hartă"""
    print("🔍 Debug Map Data")
    print("=" * 50)
    
    # Verifică numărul total de lacuri
    total_lakes = Lake.objects.count()
    active_lakes = Lake.objects.filter(is_active=True).count()
    
    print(f"📊 Total lacuri în baza de date: {total_lakes}")
    print(f"✅ Lacuri active: {active_lakes}")
    print(f"❌ Lacuri inactive: {total_lakes - active_lakes}")
    print()
    
    if active_lakes == 0:
        print("⚠️  NU EXISTĂ LACURI ACTIVE!")
        print("Aceasta este problema principală - harta nu are date de afișat.")
        return
    
    # Verifică primele 5 lacuri active
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')[:5]
    
    print("🏞️  Primele 5 lacuri active:")
    print("-" * 30)
    
    for i, lake in enumerate(lakes, 1):
        print(f"{i}. {lake.name}")
        print(f"   📍 Coordonate: {lake.latitude}, {lake.longitude}")
        print(f"   🏛️  Județ: {lake.county.name}")
        print(f"   🐟 Specii: {[fish.name for fish in lake.fish_species.all()]}")
        print(f"   💰 Preț 12h: {lake.price_12h} lei")
        print(f"   💰 Preț 24h: {lake.price_24h} lei")
        print()
    
    # Testează serializarea JSON
    print("🔧 Testez serializarea JSON...")
    try:
        lakes_data = [{
            'id': lake.id,
            'slug': lake.slug,
            'name': lake.name,
            'address': lake.address,
            'county': lake.county.name,
            'latitude': float(lake.latitude),
            'longitude': float(lake.longitude),
            'fish_species': [{'name': fish.name} for fish in lake.fish_species.all()],
            'facilities': [{'name': facility.name, 'icon_class': facility.icon_class} for facility in lake.facilities.all()],
            'price_12h': float(lake.price_12h),
            'price_24h': float(lake.price_24h),
            'image_url': lake.get_display_image().url if lake.get_display_image() else '/static/images/lake-placeholder.jpg',
            'average_rating': lake.average_rating,
            'total_reviews': lake.total_reviews
        } for lake in lakes]
        
        json_data = json.dumps(lakes_data)
        print(f"✅ JSON serializat cu succes ({len(json_data)} caractere)")
        print(f"📦 Primul lac în JSON:")
        print(json.dumps(lakes_data[0], indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Eroare la serializarea JSON: {e}")
    
    # Verifică județele
    print("\n🏛️  Județe disponibile:")
    print("-" * 20)
    counties = County.objects.all().order_by('name')
    for county in counties:
        lake_count = county.lakes.filter(is_active=True).count()
        print(f"• {county.name}: {lake_count} lacuri active")

if __name__ == '__main__':
    debug_map_data()
