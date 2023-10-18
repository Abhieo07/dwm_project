from django.shortcuts import render
from django.http import JsonResponse
from preprocessing.preprocess import Cleaning
import pandas as pd

# Create your views here.


def main(request):
    clean = {}
    if request.method == "POST":
        file = request.FILES.get('uploaded-file')
        if file:
            c_ins = Cleaning(file)
            clean = c_ins.cleaned_data()
            # print(clean)
        return JsonResponse({'data': clean})
    
    return render(request, 'core/main.html',{
        'options': clean.keys()
    })