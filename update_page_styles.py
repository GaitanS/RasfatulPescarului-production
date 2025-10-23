#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to update fishing_terms.html and article_list.html with green theme
"""

# Dictionary template - fishing_terms.html
FISHING_TERMS_EXTRA_CSS = '''{% block extra_css %}
<style>
.dictionary-hero {
    background: linear-gradient(135deg, #198754 0%, #20c997 100%);
    color: white;
    padding: 5rem 0 3rem;
    position: relative;
    overflow: hidden;
}

.dictionary-hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('{% static "images/hero.webp" %}') center/cover;
    opacity: 0.1;
    z-index: 1;
}

.dictionary-hero .container {
    position: relative;
    z-index: 2;
}

.dictionary-hero h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.dictionary-content {
    padding: 4rem 0;
    background: #f8f9fa;
}

.search-card {
    background: white;
    border-radius: 1rem;
    padding: 2.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.alphabet-nav {
    background: white;
    border-radius: 1rem;
    padding: 1.5rem;
    margin-bottom: 3rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.term-card {
    background: white;
    border-radius: 0.75rem;
    padding: 2rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    transition: all 0.3s ease;
    border-left: 4px solid #198754;
}

.term-card:hover {
    transform: translateX(5px);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.12);
}

.term-card h3 {
    color: #198754;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.btn-success {
    background: linear-gradient(135deg, #198754, #20c997);
    border: none;
}
</style>
{% endblock %}'''

# Blog template - article_list.html
BLOG_EXTRA_CSS = '''{% block extra_css %}
<style>
.blog-hero {
    background: linear-gradient(135deg, #198754 0%, #20c997 100%);
    color: white;
    padding: 5rem 0 3rem;
    position: relative;
    overflow: hidden;
}

.blog-hero::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('{% static "images/hero.webp" %}') center/cover;
    opacity: 0.1;
    z-index: 1;
}

.blog-hero .container {
    position: relative;
    z-index: 2;
}

.blog-hero h1 {
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
    text-shadow: 0 2px 4px rgba(0,0,0,0.3);
}

.blog-content {
    padding: 4rem 0;
    background: #f8f9fa;
}

.filter-section {
    background: white;
    border-radius: 1rem;
    padding: 2rem;
    margin-bottom: 3rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
}

.article-card {
    background: white;
    border-radius: 0.75rem;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
    height: 100%;
}

.article-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
}

.article-card .card-title {
    color: #198754;
    font-weight: 600;
}

.btn-success {
    background: linear-gradient(135deg, #198754, #20c997);
    border: none;
}
</style>
{% endblock %}'''

print("CSS blocks ready for manual insertion")
print("\n=== FISHING TERMS CSS ===")
print(FISHING_TERMS_EXTRA_CSS)
print("\n=== BLOG CSS ===")
print(BLOG_EXTRA_CSS)
