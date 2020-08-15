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
                print(published_time)
                product = Product(title=entries.title,description=entries.summary,website=entries.link,category=category,publish=published_time)
                product.save()
    else:
        feed = None
        all_products = None

    categoried = Category.objects.all()
    # formcategory = CategoryForm(instance=category)
    all_products = Product.objects.all().order_by('id')
    page = request.GET.get('page',1)
    paginator = Paginator(all_products, 5)
    try:
        all_products = paginator.page(page)
    except PageNotAnInteger:
        #if page is not an integer deliver the first page
        all_products = paginator.page(1)
    except EmptyPage:
        #if page is out of range deliver last page of results
        all_products = paginator.page(paginator.num_pages)
    return render(request, 'rss/reader.html', { 'page':page, 'all_products' : all_products, 'categoried' : categoried,})

def UpdateProduct(request, pk):
    product = Product.objects.get(pk=pk)
    form = ProductForm(instance=product)

    if request.method == 'POST':
        form = ProductForm(request.POST,instance=product)
        if form.is_valid():
            form.save()
            return redirect('/')

    
    return render(request, 'rss/product_form.html', {
                    'form' : form,
                    'form_name': form.__class__.__name__,
                    })

def DeleteProduct(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()
    return redirect('/')

def SearchProductByCategory(request):
    if request.GET.get("category"):
        category_id = request.GET["category"]
        all_products = Product.objects.filter(category_id__in=category_id).order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(all_products, 5)
        try:
            all_products = paginator.page(page)
        except PageNotAnInteger:
            #if page is not an integer deliver the first page
            all_products = paginator.page(1)
        except EmptyPage:
            #if page is out of range deliver last page of results
            all_products = paginator.page(paginator.num_pages)
        categoried = Category.objects.all()
    else:
        all_products = Product.objects.filter(category_id__in=category_id).order_by('id')
        page = request.GET.get('page')
        paginator = Paginator(all_products, 5)
        try:
            all_products = paginator.page(page)
        except PageNotAnInteger:
            #if page is not an integer deliver the first page
            all_products = paginator.page(1)
        except EmptyPage:
            #if page is out of range deliver last page of results
            all_products = paginator.page(paginator.num_pages)
        categoried = Category.objects.all()
    return render(request, 'rss/search.html', { 'page':page, 'all_products' : all_products, 'categoried' : categoried,})
            