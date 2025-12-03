#!/usr/bin/env python
"""
Script pentru verificarea deployment-ului modificărilor de prețuri
Rulează acest script pe serverul Hostinger după deployment
"""
import os
import sys
import django
from decimal import Decimal

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake
from django.db import connection

def check_database_structure():
    """Verifică structura bazei de date"""
    print("🔍 Verific structura bazei de date...")
    
    with connection.cursor() as cursor:
        # Verifică dacă noile coloane există (compatibil cu SQLite și MySQL)
        if 'sqlite' in connection.vendor:
            cursor.execute("PRAGMA table_info(main_lake)")
            columns = [row[1] for row in cursor.fetchall()]  # SQLite: row[1] este numele coloanei
        else:
            cursor.execute("DESCRIBE main_lake")
            columns = [row[0] for row in cursor.fetchall()]  # MySQL: row[0] este numele coloanei
        
        required_columns = ['price_12h', 'price_24h']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Coloane lipsă: {missing_columns}")
            return False
        else:
            print("✅ Toate coloanele necesare există")
            return True

def check_existing_data():
    """Verifică datele existente"""
    print("🔍 Verific datele existente...")
    
    total_lakes = Lake.objects.count()
    print(f"📊 Total lacuri în baza de date: {total_lakes}")
    
    if total_lakes == 0:
        print("ℹ️  Nu există lacuri în baza de date")
        return True
    
    # Verifică dacă lacurile au prețuri setate
    lakes_with_prices = Lake.objects.filter(
        price_12h__isnull=False, 
        price_24h__isnull=False
    ).count()
    
    print(f"✅ Lacuri cu prețuri setate: {lakes_with_prices}/{total_lakes}")
    
    # Afișează câteva exemple
    sample_lakes = Lake.objects.all()[:3]
    for lake in sample_lakes:
        print(f"   📍 {lake.name}: {lake.price_12h} RON/12h, {lake.price_24h} RON/24h")
    
    return True

def check_admin_functionality():
    """Verifică funcționalitatea admin"""
    print("🔍 Verific funcționalitatea admin...")
    
    try:
        from main.admin import LakeAdmin
        from django.contrib.admin.sites import site
        
        # Verifică dacă LakeAdmin este înregistrat
        if Lake in site._registry:
            admin_class = site._registry[Lake]
            print("✅ LakeAdmin este înregistrat corect")
            
            # Verifică fieldsets
            fieldsets = admin_class.fieldsets
            price_fields_found = False
            for name, options in fieldsets:
                if 'price_12h' in options.get('fields', []) and 'price_24h' in options.get('fields', []):
                    price_fields_found = True
                    break
            
            if price_fields_found:
                print("✅ Câmpurile de preț sunt configurate în admin")
            else:
                print("⚠️  Câmpurile de preț nu sunt găsite în configurația admin")
            
            return True
        else:
            print("❌ LakeAdmin nu este înregistrat")
            return False
            
    except Exception as e:
        print(f"❌ Eroare la verificarea admin: {e}")
        return False

def check_model_properties():
    """Verifică proprietățile modelului"""
    print("🔍 Verific proprietățile modelului...")
    
    try:
        # Creează un lac de test în memorie (fără să-l salveze)
        test_lake = Lake(
            name="Test Lake",
            price_12h=Decimal('30.00'),
            price_24h=Decimal('50.00')
        )
        
        # Verifică proprietatea price_per_day pentru compatibilitate
        if hasattr(test_lake, 'price_per_day'):
            price_per_day = test_lake.price_per_day
            if price_per_day == test_lake.price_24h:
                print("✅ Proprietatea price_per_day funcționează corect")
                return True
            else:
                print(f"⚠️  Proprietatea price_per_day returnează {price_per_day}, așteptat {test_lake.price_24h}")
                return False
        else:
            print("❌ Proprietatea price_per_day nu există")
            return False
            
    except Exception as e:
        print(f"❌ Eroare la verificarea proprietăților: {e}")
        return False

def run_all_checks():
    """Rulează toate verificările"""
    print("🚀 Încep verificarea deployment-ului...\n")
    
    checks = [
        ("Structura bazei de date", check_database_structure),
        ("Date existente", check_existing_data),
        ("Funcționalitatea admin", check_admin_functionality),
        ("Proprietățile modelului", check_model_properties),
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n{'='*50}")
        print(f"🔍 {check_name}")
        print('='*50)
        
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Eroare la {check_name}: {e}")
            results.append((check_name, False))
    
    # Sumar final
    print(f"\n{'='*50}")
    print("📊 SUMAR VERIFICĂRI")
    print('='*50)
    
    all_passed = True
    for check_name, result in results:
        status = "✅ TRECUT" if result else "❌ EȘUAT"
        print(f"{status} - {check_name}")
        if not result:
            all_passed = False
    
    print(f"\n{'='*50}")
    if all_passed:
        print("🎉 TOATE VERIFICĂRILE AU TRECUT!")
        print("✅ Deployment-ul a fost realizat cu succes!")
        print("\n🎯 Următorii pași:")
        print("   1. Testează site-ul în browser")
        print("   2. Verifică panoul de administrare")
        print("   3. Testează crearea/editarea lacurilor")
    else:
        print("⚠️  UNELE VERIFICĂRI AU EȘUAT!")
        print("🔧 Te rog să verifici erorile de mai sus și să corectezi problemele.")
    print('='*50)
    
    return all_passed

if __name__ == '__main__':
    success = run_all_checks()
    sys.exit(0 if success else 1)
