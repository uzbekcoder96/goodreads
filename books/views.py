
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect, render
from django.views import View
from books.models import Book, BookReview
from django.core.paginator import Paginator
from .forms import BookReviewForms
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.




# class BooksView(ListView):
#     template_name = 'books/list.html'
#     queryset = Book.objects.all()
#     context_object_name = 'books'
#     paginate_by = 2
    


# 2-xil usulda viewlarni yaratish mumkin yuqoridagi tayyor kod orqali yoki quyidagi qo'lda yozganimiz kabi

class BooksView(View):
    def get(self, request):
        books = Book.objects.all().order_by('id')
        search_query = request.GET.get('search', '')
        if search_query:
            books = books.filter(title__icontains=search_query)
        
        page_size = request.GET.get('page_size', 2) #default qiymat(2)
        paginator = Paginator(books, page_size)
        page_num = request.GET.get('page', 1 )  #default qiymat(1)
        
        page_obj = paginator.get_page(page_num)
        
        return render(request, 'books/list.html', {'page_obj': page_obj, 'search_query': search_query})

# class BookDetailView(DetailView):
#     template_name = 'books/detail.html'
#     pk_url_kwarg = 'id'
#     model = Book


class BookDetailView(View):
    def get(self, request, id):
        book = Book.objects.get(id=id)
        review_form = BookReviewForms()


        return render(request, 'books/detail.html', {'book':book, 'review_form': review_form })

class AddReviewView(LoginRequiredMixin, View):
    def post(self, request, id):
        book = Book.objects.get(id=id)
        review_form =  BookReviewForms(data=request.POST)
        
        if review_form.is_valid():
            BookReview.objects.create(
                book = book,
                user = request.user,
                stars_given = review_form.cleaned_data['stars_given'],
                comment = review_form.cleaned_data['comment']
            )

            return redirect(reverse('books:detail', kwargs={'id':book.id}))

        return render(request, 'books/detail.html', {'book':book, 'review_form': review_form})    

class EditReviewView(LoginRequiredMixin, View):   
    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form =  BookReviewForms(instance=review)


        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'review_form':review_form})
    def post(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)
        review_form =  BookReviewForms(instance=review, data=request.POST)

        if review_form.is_valid():
            review_form.save()
            return redirect(reverse('books:detail', kwargs={'id':book.id}))

        return render(request, 'books/edit_review.html', {'book':book, 'review':review, 'review_form':review_form})

class DeleteReviewConfirmView(LoginRequiredMixin, View):  

    def get(self, request, book_id, review_id):
        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id)     
        return render(request, 'books/delete_review_confirm.html', {'book':book, 'review':review})

class DeleteReviewView(LoginRequiredMixin, View):

    def get(self, request, book_id, review_id):

        book = Book.objects.get(id=book_id)
        review = book.bookreview_set.get(id=review_id) 

        review.delete()
        messages.success(request, 'You successfully deleted this review...')
        return redirect(reverse('books:detail', kwargs={'id':book.id}))
