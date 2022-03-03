from pyexpat import model
from rest_framework import serializers

from books.models import Book, CustomUser, BookReview

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book 
        fields = ('id', 'title', 'descriptions', 'isbn')

    
    
    # title = serializers.CharField(max_length = 200)
    # descriptions = serializers.CharField()
    # isbn = serializers.CharField(max_length = 17)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'first_name', 'last_name', 'email')


   


    # username = serializers.CharField(max_length = 200)
    # first_name = serializers.CharField(max_length = 200)
    # last_name = serializers.CharField(max_length = 200)
    # email = serializers.EmailField()




class BookReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    book = BookSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True)
    book_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = BookReview
        
        fields = ('id', 'stars_given', 'comment', 'user', 'book', 'user_id', 'book_id')
        
    
    # stars_given = serializers.IntegerField(min_value=1, max_value=5)
    # comment = serializers.CharField()

    