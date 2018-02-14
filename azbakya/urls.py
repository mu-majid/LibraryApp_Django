from django.urls import path,re_path
from . import views
from django.contrib.auth.views import logout


app_name = 'azbakya'

urlpatterns = [
    path('' , views.index , name = 'index'),
    re_path('^authors' , views.author_list_view.as_view() , name = 'authors'),
    path('author/<pk>/' , views.author_detail_view.as_view() , name = 'authorDetail'),
    path('categories/' , views.category_list_view.as_view() , name = 'categories'),
    path('follow/<authorID>' , views.follow , name = 'follow'),
    path('unfollow/<authorID>' , views.unfollow , name = 'unfollow'),
    path('profile/<username>', views.get_user_profile, name='profile'),
    path('logout/', logout , {'next_page' : '/azbakya/signin/'}, name='logout'),
    re_path(r'.*/\?q=.*', views.search, name='search'),
    path('cat_fav/<categoryID>' , views.cat_fav , name = 'cat_fav'),
    re_path('^books' , views.book_list_view.as_view() , name = 'books'),
    path('book/<pk>/' , views.book_detail_view.as_view() , name = 'bookDetail'),
    path('register/' , views.register , name = 'register'),
    path('signin/' , views.signin , name = 'signin'),
    path('mark_read/<bookID>' , views.mark_read , name = 'mark_read'),
    path('already_read/<bookID>' , views.already_read, name = 'already_read'),
    path('add_wish/<bookID>' , views.add_wish , name = 'add_wish'),
    path('remove_wish/<bookID>' , views.remove_wish, name = 'remove_wish'),
    path('rating/<bookID>', views.rating, name='rating'),


]
