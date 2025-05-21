from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, "homepage/homepage.html")

def about_view(request):
    return render(request, 'homepage/about.html')