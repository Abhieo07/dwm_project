from django.shortcuts import render
from preprocessing.preprocess import Cleaning

# Create your views here.

def main(request):
    clean = "Not cleaned"
    if request.method == "POST":
        file = request.FILES.get('uploaded-file')
        if file:
            c_ins = Cleaning(file)
            clean = c_ins.clean()
    return render(request, 'core/main.html',{
        'clean':clean
    })