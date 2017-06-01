from django.shortcuts import render

# Create your views here.

def post_list(request):
    return render(request, 'drug_test/post_list.html', {})



