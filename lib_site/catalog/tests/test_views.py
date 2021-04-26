from django.test import TestCase

from catalog.models import Author
from django.urls import reverse


class AuthorListViewTest(TestCase):

	@classmethod
	def setUpTestData(self):
		number_of_authors = 13
		for author_num in range(number_of_authors):
			Author.objects.create(
						first_name = 'Christian %s' % author_num,
						last_name = 'Surname %s' % author_num,
					)

	def test_view_url_exists_at_desired_location(self):
		resp = self.client.get('/catalog/authors/')
		self.assertEqual(resp.status_code, 200)

	def test_view_url_accessible_by_name(self):
		resp = self.client.get(reverse('authors'))
		self.assertEqual(resp.status_code, 200)

	def test_view_uses_correct_template(self):
		resp = self.client.get(reverse('authors'))
		self.assertEqual(resp.status_code, 200)

		self.assertTemplateUsed(resp, 'catalog/author_list.html')

	def test_pagination_is_ten(self):
		resp = self.client.get(reverse('authors'))
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('is_paginated' in resp.context)
		self.assertTrue(resp.context['is_paginated'] == True)
		#self.assertTrue(len(resp.context['author_list']) == 10)

	def test_lists_all_authors(self):
		resp = self.client.get(reverse('authors') + '?page=2')
		self.assertEqual(resp.status_code, 200)
		self.assertTrue('is_paginated' in resp.context)
		self.assertTrue(resp.context['is_paginated'] == True)
		#print(len(resp.context['author_list']))
		self.assertTrue( len(resp.context['author_list']) == 3)


import datetime
from django.utils import timezone

from catalog.models import BookInstance, Book, Genre
from django.contrib.auth.models import User
from django.test import Client

class LoanedBookInstancesByUserListViewTest(TestCase):

	def SetUp(self):
		test_user1 = User.objects.create_user(username='testuser1')
		test_user1.set_password('12345')
		test_user1.save()
		test_user2 = User.objects.create_user(username='testuser2', password='12345')
		test_user2.save()

		test_author = Author.objects.create(first_name='John', last_name='Smith')
		test_genre = Genre.objects.create(name='Fantasy')
		test_book = Book.objects.create(
						title='Book Title', summary='My book summary', isbn='ABCDEFG',
						author=test_author
					)
		genre_objects_for_book = Genre.objects.all()
		test_book.genre.set(genre_objects_for_book)
		test_book.save()

		#Creating 30 objects of Bookinstance
		number_of_book_copies = 30
		for book_copy in range(number_of_book_copies):
			return_date = timezone.now() + datetime.timedelta(days=book_copy % 5)
			if book_copy % 2:
				the_borrower = test_user1
			else:
				the_borrower = test_user2
			status='m'
			BookInstance.objects.create(
						book=test_book, imprint='Unlikely Imprint, 2016',
						due_back=return_date, borrower=the_borrower, status=status
					)

	def test_redirect_if_not_logged_in(self):
		resp = self.client.get(reverse('my-borrowed'))
		self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

	def test_logged_in_uses_correct_template(self):
		user = User.objects.create(username='testuser')
		user.set_password('12345')
		user.save()
		c = Client()
		log_in = c.login(username='testuser', password='12345')
		#print('Log_in:', log_in)
		#self.assertTrue(log_in)

		#login = self.client.login(username='testuser1', password='12345')
		#login = c.login(username='testuser1', password='12345')
		#resp = self.client.get(reverse('my-borrowed'), follow=True)
		#print('Test username:', resp.context['user'])
		resp = c.get(reverse('my-borrowed'), follow=True)
		
		print('Context:', resp.context['user'])
		self.assertEqual(str(resp.context['user']), 'testuser')
		self.assertEqual(resp.status_code, 200)

		print('Assert:', self.assertTemplateUsed(resp, 'catalog/bookinstance_list_borrowed_user.html'))
			# print('template is ok')
