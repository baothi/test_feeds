from django.shortcuts import render
from django.http import HttpResponse
import feedparser

# Create your views here.

def index(request):

    if request.GET.get("url"):
        url_text = request.GET["url"] #Getting URL
        url_text = url_text.replace(',',' ')
        url_text = url_text.split()
        for url in url_text:
            feed = feedparser.parse(url) #Parsing XML data
            print("11111111111111", url)
    else:
        feed = None
    return render(request, 'rss/reader.html', { 'feed' : feed,})