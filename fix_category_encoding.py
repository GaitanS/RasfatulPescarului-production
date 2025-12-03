#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to fix encoding issues in ArticleCategory names
"""
import os
import sys
import django

# Fix pentru encoding Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import ArticleCategory

def fix_category_encoding():
    """Fix encoding issues in category names"""

    # Get the category with encoding issues
    try:
        category = ArticleCategory.objects.get(slug='locatii-pescuit')

        print(f"[INFO] Found category: {category.name}")
        print(f"[INFO] Current bytes: {category.name.encode('utf-8')}")

        # Set the correct name
        category.name = 'Locații de Pescuit'
        category.save()

        # Verify the fix
        category.refresh_from_db()
        print(f"\n[OK] Updated to: {category.name}")
        print(f"[OK] New bytes: {category.name.encode('utf-8')}")

    except ArticleCategory.DoesNotExist:
        print("[ERROR] Category 'locatii-pescuit' not found")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == '__main__':
    fix_category_encoding()
