"""
Breadcrumb utilities for Răsfățul Pescarului
"""

from django.urls import reverse


class Breadcrumb:
    """Single breadcrumb item"""
    def __init__(self, name, url=None):
        self.name = name
        self.url = url


class BreadcrumbBuilder:
    """Helper class to build breadcrumbs for different pages"""
    
    @staticmethod
    def home():
        """Home page breadcrumbs"""
        return []
    
    @staticmethod
    def locations_list():
        """Locations list page breadcrumbs"""
        return [
            Breadcrumb("Locuri de Pescuit", reverse('main:locations_list'))
        ]
    
    @staticmethod
    def county_detail(county):
        """County detail page breadcrumbs"""
        return [
            Breadcrumb("Locuri de Pescuit", reverse('main:locations_list')),
            Breadcrumb(f"Județul {county.name}")
        ]
    
    @staticmethod
    def lake_detail(lake):
        """Lake detail page breadcrumbs"""
        breadcrumbs = [
            Breadcrumb("Locuri de Pescuit", reverse('main:locations_list'))
        ]
        
        if lake.county:
            breadcrumbs.append(
                Breadcrumb(
                    f"Județul {lake.county.name}",
                    reverse('main:county_detail', kwargs={'slug': lake.county.slug})
                )
            )
        
        breadcrumbs.append(Breadcrumb(lake.name))
        return breadcrumbs
    
    @staticmethod
    def solunar_calendar():
        """Solunar calendar page breadcrumbs"""
        return [
            Breadcrumb("Calendar Solunar", reverse('main:solunar_calendar'))
        ]
    
    @staticmethod
    def about():
        """About page breadcrumbs"""
        return [
            Breadcrumb("Despre Noi", reverse('main:about'))
        ]
    
    @staticmethod
    def contact():
        """Contact page breadcrumbs"""
        return [
            Breadcrumb("Contact", reverse('main:contact'))
        ]
    
    @staticmethod
    def privacy():
        """Privacy page breadcrumbs"""
        return [
            Breadcrumb("Politica de Confidențialitate", reverse('main:privacy'))
        ]
    
    @staticmethod
    def search_results(query=None):
        """Search results page breadcrumbs"""
        breadcrumbs = [
            Breadcrumb("Căutare", reverse('main:locations_list'))
        ]
        
        if query:
            breadcrumbs.append(Breadcrumb(f"Rezultate pentru: {query}"))
        else:
            breadcrumbs.append(Breadcrumb("Rezultate căutare"))
        
        return breadcrumbs
    
    @staticmethod
    def product_category(category):
        """Product category page breadcrumbs"""
        return [
            Breadcrumb("Produse", "#"),
            Breadcrumb(category.name)
        ]
    
    @staticmethod
    def product_detail(product):
        """Product detail page breadcrumbs"""
        breadcrumbs = [
            Breadcrumb("Produse", "#")
        ]
        
        if product.category:
            breadcrumbs.append(
                Breadcrumb(
                    product.category.name,
                    f"/products/category/{product.category.slug}/"
                )
            )
        
        breadcrumbs.append(Breadcrumb(product.name))
        return breadcrumbs


def add_breadcrumbs(context, breadcrumbs):
    """
    Add breadcrumbs to template context
    
    Args:
        context (dict): Template context
        breadcrumbs (list): List of Breadcrumb objects
    
    Returns:
        dict: Updated context with breadcrumbs
    """
    context['breadcrumbs'] = breadcrumbs
    return context


def get_breadcrumbs_for_view(view_name, **kwargs):
    """
    Get breadcrumbs for a specific view
    
    Args:
        view_name (str): Name of the view
        **kwargs: Additional arguments (like object instances)
    
    Returns:
        list: List of Breadcrumb objects
    """
    builder = BreadcrumbBuilder()
    
    breadcrumb_map = {
        'main:home': builder.home,
        'main:locations_list': builder.locations_list,
        'main:county_detail': lambda: builder.county_detail(kwargs.get('county')),
        'main:lake_detail': lambda: builder.lake_detail(kwargs.get('lake')),
        'main:solunar_calendar': builder.solunar_calendar,
        'main:about': builder.about,
        'main:contact': builder.contact,
        'main:privacy': builder.privacy,
    }
    
    if view_name in breadcrumb_map:
        return breadcrumb_map[view_name]()
    
    return []
