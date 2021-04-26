from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
import uuid
from datetime import date

# Create your models here.

class MyModelName(models.Model):

	# Fields
	my_field_name = models.CharField(max_length=20, help_text="Enter field documentation")

	# Metadata
	class Meta:
		ordering = ["-my_field_name"]

	# Methods
	def get_absolute_url(self):
		return reverse('model-detail-view', args=[str(self.id)])

	def __str__(self):
		return self.field_name


class Genre(models.Model):

	name = models.CharField(max_length=200,
				help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc)."
			)

	def __str__(self):
		"""String for representing the Model object (in Admin site etc.)"""
		return self.name


#class Language(models.Model):

#	name = models.CharField(max_length=200,
#				help_text="Enter a book language (English, Russian, French etc.)"
#			)

#	def __str__(self):
#		"""String for representing the Model object."""
#		return self.name


class Book(models.Model):

	title = models.CharField(max_length=200)
	author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
	isbn = models.CharField('ISBN', max_length=13,
		help_text="123 Charecter <a href=\"https://www.isbn-international.org/content/what-isbn\">ISBN number</a>")

	genre = models.ManyToManyField(Genre, help_text="Select a genre for this book")
	#language = models.OneToManyField('Language', help_text="Select a language for this book")
	#language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('book-detail', args=[str(self.id)])

	def display_genre(self):
		"""
		Creates a string for the Genre. This is required to display genre in Admin.
		"""
		return ', '.join([ genre.name for genre in self.genre.all()[:3] ])
	display_genre.short_description = 'Genre'

	def get_inst_count(self):
		return BookInstance.objects.filter(book=self).count()


class BookInstance(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4,
				help_text="Unique ID for this particular book across whole library")
	book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
	imprint = models.CharField(max_length=200)
	due_back = models.DateField(null=True, blank=True)
	borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

	LOAN_STATUS = (
		('m', 'Maintenance'),
		('o', 'On loan'),
		('a', 'Available'),
		('r', 'Reserved'),
	)

	status = models.CharField(max_length=1,
				choices=LOAN_STATUS,
				blank=True,
				default='m',
				help_text='Book availability'
				)

	class Meta:
		ordering = ["-due_back"]
		permissions = (("can_mark_returned", "Set book as returned"),)

	def __str__(self):
		return '%s (%s)' % (self.id, self.book.title)

	@property
	def is_overdue(self):
		if self.due_back and date.today() > self.due_back:
			return True
		return False


class Author(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	date_of_birth = models.DateField(null=True, blank=True)
	date_of_death = models.DateField('Died', null=True, blank=True)

	def get_absolute_url(self):
		return reverse('author-detail', args=[str(self.id)])

	def __str__(self):
		return '%s, %s' % (self.last_name, self.first_name)

	#def get_books_count(self):
	#	return Book.objects.filter(author=self).count()

	def get_books(self):
		return Book.objects.filter(author=self)

	class Meta:
		ordering = ["last_name"]

