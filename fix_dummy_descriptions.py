#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to fix dummy/placeholder descriptions in lake database
Replaces dummy text with proper descriptions
"""
import os
import sys
import django
import re

# Fix pentru encoding Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import Lake

def is_dummy_description(text):
    """Check if description appears to be dummy/placeholder text"""
    if not text or len(text.strip()) < 10:
        return True

    # Patterns that indicate dummy text
    dummy_patterns = [
        r'^[a-z]{10,}$',  # Long strings of only lowercase letters (sfdhgsdfgsdfg)
        r'^[a-z\s]{5,20}$',  # Short repetitive patterns
        r'(test|dummy|placeholder|lorem|ipsum)',  # Common placeholder words
        r'([a-z])\1{4,}',  # Same letter repeated 5+ times
    ]

    text_lower = text.lower().strip()

    for pattern in dummy_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return True

    # Check if it's mostly random characters
    unique_chars = len(set(text_lower.replace(' ', '')))
    total_chars = len(text_lower.replace(' ', ''))
    if total_chars > 10 and unique_chars < total_chars * 0.3:  # Less than 30% unique chars
        return True

    return False

def generate_description(lake):
    """Generate a proper description for a lake"""
    address_parts = lake.address.split(',')
    locality = address_parts[0].strip() if address_parts else lake.county.name

    return f"Lac de pescuit situat în {locality}, {lake.county.name}"

def fix_descriptions():
    """Fix all dummy descriptions in the database"""
    print("=" * 80)
    print("FIXARE DESCRIERI DUMMY")
    print("=" * 80)
    print()

    all_lakes = Lake.objects.all()
    fixed_count = 0
    skipped_count = 0

    print(f"[1/2] Scanez {all_lakes.count()} lacuri pentru descrieri dummy...")
    print("-" * 80)

    for lake in all_lakes:
        if is_dummy_description(lake.description):
            old_description = lake.description
            new_description = generate_description(lake)

            lake.description = new_description
            lake.save(update_fields=['description'])

            print(f"✓ Fixat: {lake.name}")
            print(f"  Vechi: '{old_description[:50]}{'...' if len(old_description) > 50 else ''}'")
            print(f"  Nou:   '{new_description}'")
            print()

            fixed_count += 1
        else:
            skipped_count += 1

    print("-" * 80)
    print()
    print("=" * 80)
    print("STATISTICI FINALE")
    print("=" * 80)
    print(f"✓ Descrieri fixate:  {fixed_count}")
    print(f"○ Descrieri OK:      {skipped_count}")
    print(f"─ Total procesate:   {all_lakes.count()}")
    print("=" * 80)
    print()

    if fixed_count > 0:
        print("✓ Descrierile dummy au fost actualizate cu succes!")
    else:
        print("○ Nu au fost găsite descrieri dummy.")
    print()

if __name__ == '__main__':
    fix_descriptions()
