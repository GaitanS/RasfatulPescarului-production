#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script pentru verificarea articolelor create in baza de date
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

from main.models import Article, ArticleCategory

def main():
    print("=" * 70)
    print("VERIFICARE ARTICOLE BLOG")
    print("=" * 70)
    print()

    # Statistici generale
    total_articles = Article.objects.count()
    published_articles = Article.objects.filter(is_published=True).count()
    featured_articles = Article.objects.filter(is_featured=True).count()

    print(f"Total articole: {total_articles}")
    print(f"Articole publicate: {published_articles}")
    print(f"Articole featured: {featured_articles}")
    print()

    # Articole pe categorii
    print("ARTICOLE PE CATEGORII:")
    print("-" * 70)

    categories = ArticleCategory.objects.all().order_by('order')
    for category in categories:
        count = Article.objects.filter(category=category, is_published=True).count()
        print(f"\n{category.name}: {count} articole")

        articles = Article.objects.filter(category=category, is_published=True).order_by('-published_date')
        for i, article in enumerate(articles, 1):
            featured_mark = " [FEATURED]" if article.is_featured else ""
            print(f"  {i}. {article.title}{featured_mark}")
            print(f"     URL: /blog/{article.slug}/")
            print(f"     Reading time: {article.reading_time} min")

    print()
    print("=" * 70)
    print("LINKURI UTILE:")
    print("=" * 70)
    print("Blog homepage: http://127.0.0.1:8000/blog/")
    print("Dictionar pescuit: http://127.0.0.1:8000/dictionar-pescuit/")
    print("Specii de pesti: http://127.0.0.1:8000/specii-de-pesti/")
    print()

if __name__ == '__main__':
    main()
