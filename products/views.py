from django.shortcuts import render
from .models import Product
from django.shortcuts import redirect 
from django.urls import reverse
from django.db import models

# Create your views here.
def index(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        if query:
            url = reverse('search')  
            return redirect(f'{url}?q={query}')  
    return render(request, 'products/index.html')

def search_results(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        
        if query:
            name_filter = models.Q()
            for keyword in query.split():
                name_filter |= models.Q(name__icontains=keyword)
                
            low = request.GET.get('lower-limit', None)
            high = request.GET.get('upper-limit', None)
            
            
            
            price_filter = models.Q()
            if low and high:
                price_filter = models.Q(price__gte=low) & models.Q(price__lte=high)
            
            brands_selected = request.GET.getlist('brands', None)
            
            brand_filter = models.Q()
            for brand in brands_selected:
                brand_filter |= models.Q(brand__icontains=brand)
            
            products_without_filters = Product.objects.filter(
                name_filter,
            )
            
            brands = products_without_filters.values_list('brand', flat=True).distinct()
            
            brands = {brand: True if brand in brands_selected else False for brand in brands}
            print(brands)
            
            products = products_without_filters.filter(
                brand_filter,
                price_filter,
            )
            
            filtering = request.GET.get('filtering', False)
            
            if request.headers.get('HX-Request', False) or filtering:
                print("YAY",filtering)
                return render(request, 'products/partials/search_results.html', context={'products': products, "brands": brands})
            else:
                return render(request, 'products/main.html', context={'products': products, 'query': query, "brands": brands})
    
        return render(request, 'products/main.html')