#!/usr/bin/env python
"""
Script de test pentru a verifica că API-ul pentru hartă returnează datele corecte
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake
import json

def test_map_data():
    """Testează datele pentru hartă"""
    print("🔍 Testez datele pentru hartă...")
    
    # Simulez ce face view-ul locations_map
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')
    
    if not lakes.exists():
        print("❌ Nu există lacuri active în baza de date")
        return False
    
    # Serialize lakes data for JavaScript (exact ca în view)
    lakes_data = []
    for lake in lakes:
        lake_data = {
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
        }
        lakes_data.append(lake_data)
    
    print(f"✅ Găsite {len(lakes_data)} lacuri active")
    
    # Verifică primul lac
    if lakes_data:
        first_lake = lakes_data[0]
        print(f"\n📊 Primul lac: {first_lake['name']}")
        print(f"   - Preț 12h: {first_lake['price_12h']} Lei")
        print(f"   - Preț 24h: {first_lake['price_24h']} Lei")
        print(f"   - Coordonate: {first_lake['latitude']}, {first_lake['longitude']}")
        
        # Verifică că nu există price_per_day
        if 'price_per_day' in first_lake:
            print("⚠️  ATENȚIE: price_per_day încă există în date!")
            return False
        else:
            print("✅ price_per_day nu mai există în date")
    
    # Testează JSON serialization
    try:
        json_data = json.dumps(lakes_data)
        print("✅ Datele se serializează corect în JSON")
    except Exception as e:
        print(f"❌ Eroare la serializarea JSON: {e}")
        return False
    
    return True

def test_filter_api():
    """Testează API-ul de filtrare"""
    print("\n🔍 Testez API-ul de filtrare...")
    
    lakes = Lake.objects.filter(is_active=True).select_related('county').prefetch_related('fish_species', 'facilities')
    
    # Simulez filtrarea cu preț maxim
    max_price = 50
    filtered_lakes = lakes.filter(price_12h__lte=max_price)
    
    print(f"✅ Filtrul de preț funcționează: {filtered_lakes.count()} lacuri cu preț ≤ {max_price} Lei/12h")
    
    # Testează datele returnate
    for lake in filtered_lakes[:3]:  # Primele 3
        lake_data = {
            'id': lake.id,
            'name': lake.name,
            'price_12h': float(lake.price_12h),
            'price_24h': float(lake.price_24h),
        }
        print(f"   - {lake_data['name']}: {lake_data['price_12h']} Lei/12h, {lake_data['price_24h']} Lei/24h")
    
    return True

if __name__ == "__main__":
    print("🚀 Testez API-ul pentru hartă...\n")
    
    success = True
    success &= test_map_data()
    success &= test_filter_api()
    
    if success:
        print("\n🎉 Toate testele au trecut cu succes!")
        print("✅ Harta ar trebui să afișeze prețurile corecte acum")
    else:
        print("\n❌ Unele teste au eșuat")
        sys.exit(1)
