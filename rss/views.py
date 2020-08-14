from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import feedparser

from .models import Category, Product

# Create your views here.

def index(request):

    if request.GET.get("url"):
        url_text = request.GET["url"] #Getting URL
        url_text = url_text.replace(',',' ')
        url_text = url_text.split()
        for url in url_text:
            u = url.split('/')
            print("11111111111111", u[-1])
            if not Category.objects.filter(name=u[-1]).exists():
                categoried = Category(name=u[-1])
                categoried.save()
            category = Category.objects.get(name=u[-1])
            
            feed = feedparser.parse(url) #Parsing XML data
            for entries in feed.entries:
                product = Product(title=entries.title,description=entries.summary,website=entries.link,category=category)
                product.save()
        all_products = Product.objects.all()
    else:
        feed = None
        all_products = None
    return render(request, 'rss/reader.html', { 'feed' : feed,'all_products' : all_products, })