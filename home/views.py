from django.shortcuts import render

# Create your views here.
class HomeView:
    def get(self, request):
        return render(request, 'home/index.html')