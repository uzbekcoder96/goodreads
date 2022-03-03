import email
from django.test import TestCase
from books.models import BookAuthor, Book, Author
from django.urls import reverse

from users.models import CustomUser

class BookTestCase(TestCase):


    def test_book_not_founded(self):
        response = self.client.get(reverse('books:list'))

        self.assertContains(response, 'Books not founded.')
       
    def test_books_list(self):

        book1 = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123')   
        book2 = Book.objects.create(title='Book2', descriptions='Description2', isbn='1111111')
        book3 = Book.objects.create(title='Book3', descriptions='Description3', isbn='2222222')


        respon = self.client.get(
            reverse('books:list') + '?page_size=2',
        )

        
        for book in [book1, book2]:
            self.assertContains(respon, book.title)

        respon = self.client.get(reverse('books:list') + '?page=2&page_size=2')

        self.assertContains(respon, book3.title)


    def test_detail_page(self):
        book = Book.objects.create(title='Book3', descriptions='Description3', isbn='2222222')
        author = Author.objects.create(first_name='Garry', last_name='Potter', email='garri@gmail.com', bio='something about author')
        book_author = BookAuthor.objects.create(book=book, author=author)
        response = self.client.get(reverse('books:detail', kwargs={'id': book.id}))
       

        self.assertContains(response, book.title)
        self.assertContains(response, book.descriptions)
        self.assertContains(response, book_author.author.full_name())


    def test_search_books(self):

        book1 = Book.objects.create(title='sport', descriptions='Description1', isbn='123123')   
        book2 = Book.objects.create(title='game', descriptions='Description2', isbn='1111111')
        book3 = Book.objects.create(title='football', descriptions='Description3', isbn='2222222')

        response = self.client.get(reverse('books:list') + '?search=sport')
        self.assertContains(response, book1.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books:list') + '?search=game')
        self.assertContains(response, book2.title)
        self.assertNotContains(response, book1.title)
        self.assertNotContains(response, book3.title)


        response = self.client.get(reverse('books:list') + '?search=football')
        self.assertContains(response, book3.title)
        self.assertNotContains(response, book2.title)
        self.assertNotContains(response, book1.title)


class ReviewTestCase(TestCase):
    def test_reviews(self):
        book = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123')   
        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir', email='example@gmail.com')
        user.set_password("somepassword")
        user.save()
        self.client.login(username='jahongir', password='somepassword')

        self.client.post(reverse('books:review', kwargs={'id':book.id}),data= {
            'stars_given': 3,
            'comment': 'Nice book'
            }
        )
        
        book_review = book.bookreview_set.all()

        self.assertEqual(book_review.count(), 1)
        self.assertEqual(book_review[0].stars_given, 3)
        self.assertEqual(book_review[0].comment, 'Nice book')
        self.assertEqual(book_review[0].book, book)
        self.assertEqual(book_review[0].user, user)

    def test_update_review(self):

        book = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123')   
        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir', email='example@gmail.com')
        user.set_password("somepassword")
        user.save()
        self.client.login(username='jahongir', password='somepassword')
        self.client.post(reverse('books:review', kwargs={'id':book.id}),data= {
            'stars_given': 3,
            'comment': 'Nice book'
            }
        )
        book_review = book.bookreview_set.all()
        review1 = book_review[0]
        
        self.client.get(reverse('books:edit-review', kwargs={'book_id':book.id, 'review_id':review1.id} ))

        response = self.client.post(reverse('books:edit-review', kwargs={'book_id':book.id, 'review_id':review1.id}),data= {
            'stars_given': 5,
            'comment': 'Good book'
            }
        )
        book.refresh_from_db()

        book_review = book.bookreview_set.all()
        review2 = book_review[0]
        
        self.client.get(reverse('books:edit-review', kwargs={'book_id':book.id, 'review_id':review2.id} ))
        
        self.assertEqual(review1.comment, 'Nice book')
        self.assertEqual(review1.stars_given, 3)

        self.assertEqual(review2.comment, 'Good book')
        self.assertEqual(review2.stars_given, 5)


        self.assertEqual(response.url, reverse('books:detail', kwargs={'id':book.id}))

    def test_delete_review_confirm(self):

        book = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123')   
        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir', email='example@gmail.com')
        user.set_password("somepassword")
        user.save()
        self.client.login(username='jahongir', password='somepassword')
        response = self.client.post(reverse('books:review', kwargs={'id':book.id}),data= {
            'stars_given': 3,
            'comment': 'Nice book'
            }
        )    
        book_review = book.bookreview_set.all()
        review2 = book_review[0]

        self.client.get(reverse('books:delete-review-confirm', kwargs={'book_id':book.id, 'review_id':review2.id} ))    

        self.assertEqual(book.title, 'Book1')
        self.assertEqual(review2.comment, 'Nice book')
        self.assertEqual(review2.stars_given, 3)
        print(response.url)
        # self.assertEqual(response.url, reverse('books:delete-review', kwargs={'book_id':book.id,'review_id':review2.id}))

    def test_delete_review(self):
        
        book = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123')   
        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir', email='example@gmail.com')
        user.set_password("somepassword")
        user.save()
        self.client.login(username='jahongir', password='somepassword')
        response = self.client.post(reverse('books:review', kwargs={'id':book.id}),data= {
            'stars_given': 3,
            'comment': 'Nice book'
            }
        )    
        book_review = book.bookreview_set.all()
        review2 = book_review[0]

        self.client.get(reverse('books:delete-review', kwargs={'book_id':book.id, 'review_id':review2.id} ))  
        
        self.assertIsNone(review2)