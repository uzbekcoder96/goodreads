from django.urls import reverse
from django.test import TestCase
from books.models import Book, BookReview
from users.models import CustomUser

class HomePageTestCase(TestCase):
    def test_paginated_list(self):
        book = Book.objects.create(title='Book1', descriptions='Description1', isbn='123123') 

        user = CustomUser.objects.create(username='jahongir', first_name='Jahongir')
        user.set_password("somepassword")
        user.save()

        review1 = BookReview.objects.create(book=book, user=user, stars_given=3, comment="Very helpful book")
        review2 = BookReview.objects.create(book=book, user=user, stars_given=5, comment="Very userful book")
        review3 = BookReview.objects.create(book=book, user=user, stars_given=2, comment="Great book")
        
        response = self.client.get(reverse('home_page')+'?page_size=2')
        self.assertContains(response, review2.comment)
        self.assertContains(response, review3.comment)
