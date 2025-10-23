#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to fix encoding issues in articles
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

from main.models import Article

def fix_encoding():
    """Fix encoding issues in article titles and content"""

    # Get all articles with potential encoding issues
    articles = Article.objects.all()

    fixed_count = 0

    for article in articles:
        original_title = article.title
        original_excerpt = article.excerpt
        original_content = article.content

        # Fix common encoding issues
        replacements = {
            'Ã®': 'î',
            'Ã¢': 'â',
            'Ã¢': 'â',
            'Ä': 'ă',
            'È': 'ș',
            'È': 'ț',
            'Å': 'Ș',
            'Å': 'Ț',
        }

        # Fix title
        new_title = original_title
        for wrong, correct in replacements.items():
            new_title = new_title.replace(wrong, correct)

        # Fix excerpt
        new_excerpt = original_excerpt
        for wrong, correct in replacements.items():
            new_excerpt = new_excerpt.replace(wrong, correct)

        # Fix content
        new_content = original_content
        for wrong, correct in replacements.items():
            new_content = new_content.replace(wrong, correct)

        # Update if changed
        if new_title != original_title or new_excerpt != original_excerpt or new_content != original_content:
            article.title = new_title
            article.excerpt = new_excerpt
            article.content = new_content
            article.save()
            fixed_count += 1
            print(f"[OK] Fixed: {article.id}. {original_title} -> {new_title}")

    print(f"\n[DONE] Fixed {fixed_count} articles")
    print(f"[INFO] Total articles: {Article.objects.count()}")

if __name__ == '__main__':
    fix_encoding()
