from django.db import models
from django.urls import reverse # this will be used to generate URLs by reversing the urls patterns
import uuid
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    '''
    model representing a book genre
    '''
    name=models.CharField(max_length=200, help_text="enter a book genre")
    def __str__(self):
        """
        string for representing the model object(in admin site)
        """
        return self.name
class Book(models.Model):
    """
    model representing a book
    """
    title=models.CharField(max_length=200)
    author=models.ForeignKey('author', on_delete=models.SET_NULL, null=True)
    #we use ForeignKey cause every book can have one author, but authors can have multiple Book
    summary=models.TextField(max_length=1000, help_text='enter a brief description of the book')
    isbn=models.CharField('ISBN', max_length=200, help_text="13 character")
    genre=models.ManyToManyField(Genre, help_text="select a genre for this book")
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        returns the url to access a particular book instance
        """
        return reverse('book-detail', args=[str(self.id)])
class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ["due_back"]


    def __str__(self):
        """
        String for representing the Model object
        """
        return '%s (%s)' % (self.id,self.book.title)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('catalog:author-detail', args=[str(self.id)])


    def __str__(self):
        """
        String for representing the Model object.
        """
        return '%s, %s' % (self.last_name, self.first_name)
