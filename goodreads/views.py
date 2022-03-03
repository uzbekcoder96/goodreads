from django.shortcuts import redirect, render
from books.models import BookReview
from django.core.paginator import Paginator


def landing(request):
    return render(request, 'landing.html')



def home_page(request):
    books_reviews = BookReview.objects.all().order_by('-created_at')

    page_size = request.GET.get('page_size', 10) #default qiymat(2)
    paginator = Paginator(books_reviews, page_size)
    page_num = request.GET.get('page', 1 )  #default qiymat(1)
    
    page_obj = paginator.get_page(page_num)

    return render(request, 'home.html', { 'page_obj':page_obj})
    