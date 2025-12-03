#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import django

# Fix encoding
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RasfatulPescarului.settings')
django.setup()

from main.models import County

counties = County.objects.all().order_by('name')
print(f"Total counties: {counties.count()}\n")
for c in counties:
    guide_status = "YES" if c.guide_content else "NO"
    print(f"{c.slug:20} - {c.name:20} - Guide: {guide_status}")
