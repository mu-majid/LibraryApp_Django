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

]
