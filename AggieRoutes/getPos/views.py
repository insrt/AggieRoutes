from django.shortcuts import render


#def post(self, request):
 #   print(request.post)

def home_view(request, *args, **kwargs):
    print(request.POST)
    return render(request, "index.html")