from .models import *
from django.contrib.auth.models import User
from django.views.generic import DetailView,ListView
from django.contrib.auth import login, authenticate ,logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import SignUpForm,ProfileForm,SignInForm
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.http import Http404, HttpResponse
import json

def index(request):
    return render(request, 'azbakya/index.html' )

def get_user_profile(request, username):
    user = User.objects.get(username=username)
    image = profile.objects.get(user=user).image
    books_read = UserBookRead.objects.filter(user=user)
    books_wish = UserBookWish.objects.filter(user=user)
    author_follow = UserAuthor.objects.filter(user=user)
    return render(request, 'azbakya/user.html', {'user': user,'image': image,'books_read':books_read,'books_wish':books_wish,'author_follow':author_follow})

class user_detail_view(DetailView):
    model = User

class author_list_view(ListView):
    model = Author
    paginate_by = 9
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        authors = UserAuthor.objects.filter(user=self.request.user)
        result = []
        for i,author in enumerate(authors):
            result.append(authors[i].author)
        context['author_follow']= result
        return context

class author_detail_view(DetailView):
    model = Author
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        authors = UserAuthor.objects.filter(user=self.request.user)
        result = []
        for i,author in enumerate(authors):
            result.append(authors[i].author)
        context['author_follow']= result
        return context

class category_list_view(ListView):
    model = Category

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        cat_fav = CategoryUser.objects.filter(user=self.request.user)
        result = []
        for i,category in enumerate(cat_fav):
            result.append(cat_fav[i].category)
        context['cat_fav']= result

        return context

def search(request):
    if 'q' in request.GET :
        q = request.GET['q']
        books = Book.objects.filter(title__icontains=q)
        authors = Author.objects.filter(name__icontains=q)
        return render(request, 'azbakya/search_result.html',
        {'authors': authors, 'books': books, 'query': q})

def follow(request,authorID):
    authorIns = Author.objects.get(pk=authorID)
    record = UserAuthor(author = authorIns,user = request.user)
    record.save()
    data = {}
    return JsonResponse(data)

def unfollow(request,authorID):
    authorIns = Author.objects.get(pk=authorID)
    record = UserAuthor.objects.get(author = authorIns,user = request.user)
    record.delete()
    data = {}
    return JsonResponse(data)

def cat_fav(request,categoryID):
    referer = request.META.get('HTTP_REFERER')
    catIns = Category.objects.get(pk=categoryID)
    if(CategoryUser.objects.filter(category=catIns,user=request.user)):
        record = CategoryUser.objects.get(category=catIns,user=request.user)
        record.delete()
    else:
        record = CategoryUser(category=catIns,user=request.user)
        record.save()
    return redirect(referer)
