from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import feedparser
from .forms import *

from .models import Category, Product
from django.views.generic import TemplateView, ListView
import datetime
import dateutil.parser

# Create your views here.

def index(request):

    if request.GET.get("url"):
        url_text = request.GET["url"] #Getting URL
        url_text = url_text.replace(',',' ')
        url_text = url_text.split()
        for url in url_text:
            u = url.split('/')
            if not Category.objects.filter(name=u[-1]).exists():
                categoried = Category(name=u[-1])
                categoried.save()
            category = Category.objects.get(name=u[-1])
            
            feed = feedparser.parse(url) #Parsing XML data
            for entries in feed.entries:
                published_time = dateutil.parser.parse(entries.published)
                product = Product(title=entries.title,description=entries.summary,website=entries.link,category=category,publish=published_time)
                product.save()
    else:
        all_products = None

    
    PAGESIZE = 5
    category_id = request.GET.get("category", "")
    category_id = int(category_id) if category_id else ''
    all_products = Product.objects.all()
    
    if category_id:
        all_products = all_products.filter(category_id=category_id)
    
    all_products = all_products.order_by('id')
    paginator = Paginator(all_products, PAGESIZE)

    page = int(request.GET.get('page', 1))
    page = max(min(page, paginator.num_pages), 1)    
    all_products = paginator.page(page)
       
    return render(request, 'rss/reader.html', 
        { 
            'page':page, 
            'offset': (page-1)* PAGESIZE,
            'all_products' : all_products, 
            'categoried' : Category.objects.all(),
            'selected_category': category_id
        })

def UpdateProduct(request, pk):
    page = request.GET.get("page", "")
    category = request.GET.get("category", "")
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        page_id = request.POST['page']
        page_id = int(page_id) if page_id else ''
        category_id = request.POST['category']
        category_id = int(category_id) if category_id else ''
        if form.is_valid():
            form.save()
            return redirect('/?page='+str(page_id)+'&category='+str(category_id))

    
    return render(request, 'rss/product_form.html', {
                    'form' : form,
                    'form_name': form.__class__.__name__,
                    'product_id': product.id,
                    'page': page,
                    'category': category,
                    })

def DeleteProduct(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('/')
