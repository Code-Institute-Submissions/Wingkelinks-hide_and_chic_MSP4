from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib import messages
from django.db.models import Q
from django.db.models.functions import Lower
# Q from Django to handle filtering search by name and or description
from .models import Category, Product
from .forms import ProductForm


def all_products(request):
    """ 
    A view to show all products, including sorting categories and handling search queries.
    """
    
    products = Product.objects.all()
    query = None
    categories = None
    sort = None
    direction = None
    sale = False
    
    if request.GET:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                products = products.annotate(lower_name=Lower('name'))
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            products = products.order_by(sortkey)
    
        if request.GET:
            if 'category' in request.GET:
                categories = request.GET['category'].split(',')
                products = products.filter(category__name__in=categories)
                categories = Category.objects.filter(name__in=categories)

            if 'q' in request.GET:
                query = request.GET['q']
                if not query:
                    messages.error(request, "You didn't enter any search criteria!")
                    return redirect(reverse('products'))
                
                queries = Q(name__icontains=query) | Q(description__icontains=query)
                products = products.filter(queries)
                
            if 'sale' in request.GET:
                sale = True
                products = products.filter(on_sale=True)
    
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'sale': sale,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    """ A view to show individual product details """
    
    # To only return one product
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)

def add_product(request):
    """ Add a product to the database """
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('add_product'))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)