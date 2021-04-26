from django.urls import path, re_path
from . import views
from django.conf.urls import url

urlpatterns = [
	#path('', views.index, name='index'),
	#path('books/', views.BookListView.as_view(), name='books'),
	url(r'^$', views.index, name='index'),
	url(r'^books/$', views.BookListView.as_view(), name='books'),
	re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
	path('author/', views.AuthorListView.as_view(), name='authors'),
	re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
	#re_path(r'^/url/$', views.my_reused_view, {'my_template_name': 'some_path'}, name='aurl'),
	#re_path(r'^/anotherurl/$', views.my_reused_view, {'my_template_name': 'another_path'}, name='anotherurl'),
]

urlpatterns += [
	url(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
	url(r'^borrowed/$', views.LoanedBooksByAllUsersListView.as_view(), name='all-borrowed'),
	url(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name='renew-book-librarian'),
]

urlpatterns += [
	url(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
	url(r'^author/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
	url(r'^author/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
]

urlpatterns += [
	url(r'^books/create/$', views.BookCreate.as_view(), name='book_create'),
	url(r'^books/(?P<pk>\d+)/update/$', views.BookUpdate.as_view(), name='book_update'),
	url(r'^books/(?P<pk>\d+)/delete/$', views.BookDelete.as_view(), name='book_delete'),
]
