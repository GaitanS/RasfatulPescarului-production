"""
SEO Template Tags for Răsfățul Pescarului
"""

import json
from django import template
from django.utils.safestring import mark_safe
from django.urls import reverse

register = template.Library()


@register.simple_tag
def structured_data_website():
    """Generate structured data for the website"""
    data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "Răsfățul Pescarului",
        "url": "https://rasfatul-pescarului.ro",
        "description": "Descoperă cele mai bune locuri de pescuit din România, echipamente de calitate și calendarul solunar pentru pescuit.",
        "potentialAction": {
            "@type": "SearchAction",
            "target": "https://rasfatul-pescarului.ro/search?q={search_term_string}",
            "query-input": "required name=search_term_string"
        },
        "publisher": {
            "@type": "Organization",
            "name": "Răsfățul Pescarului",
            "url": "https://rasfatul-pescarului.ro"
        }
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


@register.simple_tag
def structured_data_lake(lake):
    """Generate structured data for a lake"""
    if not lake:
        return ""
    
    data = {
        "@context": "https://schema.org",
        "@type": "Place",
        "name": lake.name,
        "description": lake.description or f"Lac de pescuit în {lake.county.name if lake.county else 'România'}",
        "url": f"https://rasfatul-pescarului.ro/locations/lake/{lake.slug}/",
        "address": {
            "@type": "PostalAddress",
            "addressCountry": "RO"
        }
    }
    
    if lake.county:
        data["address"]["addressRegion"] = lake.county.name
    
    if hasattr(lake, 'latitude') and hasattr(lake, 'longitude') and lake.latitude and lake.longitude:
        data["geo"] = {
            "@type": "GeoCoordinates",
            "latitude": float(lake.latitude),
            "longitude": float(lake.longitude)
        }
    
    if hasattr(lake, 'image') and lake.image:
        data["image"] = f"https://rasfatul-pescarului.ro{lake.image.url}"
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


@register.simple_tag
def structured_data_organization():
    """Generate structured data for the organization"""
    data = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "Răsfățul Pescarului",
        "url": "https://rasfatul-pescarului.ro",
        "description": "Comunitatea pescarilor din România - ghid complet pentru locuri de pescuit și echipamente",
        "logo": "https://rasfatul-pescarului.ro/static/images/logo.png",
        "contactPoint": {
            "@type": "ContactPoint",
            "contactType": "customer service",
            "email": "contact@rasfatul-pescarului.ro"
        },
        "sameAs": [
            "https://www.facebook.com/rasfatulpescarului",
            "https://www.tiktok.com/@rasfatulpescarului"
        ]
    }
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


@register.simple_tag
def structured_data_breadcrumbs(breadcrumbs, current_url):
    """Generate structured data for breadcrumbs"""
    if not breadcrumbs:
        return ""
    
    items = [{
        "@type": "ListItem",
        "position": 1,
        "name": "Acasă",
        "item": "https://rasfatul-pescarului.ro/"
    }]
    
    for i, breadcrumb in enumerate(breadcrumbs, 2):
        item = {
            "@type": "ListItem",
            "position": i,
            "name": breadcrumb.name
        }
        
        if breadcrumb.url and i < len(breadcrumbs) + 1:
            item["item"] = f"https://rasfatul-pescarului.ro{breadcrumb.url}"
        else:
            item["item"] = current_url
        
        items.append(item)
    
    data = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items
    }
    
    return mark_safe(f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>')


@register.simple_tag
def meta_description(description, max_length=160):
    """Generate meta description with proper length"""
    if not description:
        return "Descoperă cele mai bune locuri de pescuit din România, echipamente de calitate și calendarul solunar pentru pescuit."
    
    if len(description) > max_length:
        # Truncate at word boundary
        truncated = description[:max_length].rsplit(' ', 1)[0]
        return f"{truncated}..."
    
    return description


@register.simple_tag
def meta_keywords(*keywords):
    """Generate meta keywords from arguments"""
    base_keywords = [
        "pescuit", "locuri pescuit", "echipamente pescuit", 
        "calendar solunar", "pescuit România", "lacuri pescuit"
    ]
    
    all_keywords = base_keywords + list(keywords)
    return ", ".join(filter(None, all_keywords))


@register.simple_tag
def canonical_url(request, custom_url=None):
    """Generate canonical URL"""
    if custom_url:
        return custom_url
    
    return request.build_absolute_uri(request.path)


@register.simple_tag
def og_image(image_url=None):
    """Generate Open Graph image URL"""
    if image_url:
        if image_url.startswith('http'):
            return image_url
        return f"https://rasfatul-pescarului.ro{image_url}"
    
    return "https://rasfatul-pescarului.ro/static/images/logo.png"


@register.filter
def truncate_words_smart(value, length):
    """Smart truncation that preserves word boundaries"""
    if not value:
        return ""
    
    if len(value) <= length:
        return value
    
    truncated = value[:length].rsplit(' ', 1)[0]
    return f"{truncated}..."
