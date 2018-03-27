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
    cats_fav = CategoryUser.objects.filter(user=user)
    books_read = UserBookRead.objects.filter(user=user)
    books_wish = UserBookWish.objects.filter(user=user)
    author_follow = UserAuthor.objects.filter(user=user)
    return render(request, 'azbakya/user.html', {'user': user,'image': image,'cats_fav':cats_fav,'books_read':books_read,'books_wish':books_wish,'author_follow':author_follow})

class user_detail_view(DetailView):
    model = User

class author_list_view(LoginRequiredMixin,ListView):
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

class author_detail_view(LoginRequiredMixin,DetailView):
    model = Author
    login_url = '/azbakya/signin'
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        authors = UserAuthor.objects.filter(user=self.request.user)
        result = []
        for i,author in enumerate(authors):
            result.append(authors[i].author)
        context['author_follow']= result
        return context

class book_list_view(LoginRequiredMixin,ListView):
    model = Book
    paginate_by = 6
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        books_read = UserBookRead.objects.filter(user=self.request.user)
        books_wish = UserBookWish.objects.filter(user=self.request.user)
        result1 = []
        result2 = []
        for i,book in enumerate(books_read):
            result1.append(books_read[i].book)
        for j,book in enumerate(books_wish):
            result2.append(books_wish[j].book)
        context['book_read']= result1
        context['book_wish']= result2
        return context

class book_detail_view(LoginRequiredMixin,DetailView):
    model = Book
    login_url = '/azbakya/signin'
    # redirect_field_name = ''
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)

        result1,result2,result3 = None,None,None

        if(UserBookRead.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))):
            result1 = UserBookRead.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))[0].book

        if(UserBookWish.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))):
            result2 = UserBookWish.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))[0].book

        if(UserBookRate.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))):
            result3 = UserBookRate.objects.filter(user=self.request.user, book=Book.objects.get(pk=self.kwargs['pk']))[0].rate
        context['book_read']= result1
        context['book_wish']= result2
        context['book_rate']= result3

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

def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST,request.FILES)
        profile_form = ProfileForm(request.POST,request.FILES)
        if form.is_valid() and profile_form.is_valid():
            form = form.save()
            profile = profile_form.save(commit=False)
            profile.user_id = form.id
            profile.save()
            return redirect('azbakya:index')
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(request, 'azbakya/register.html', {'form': form,'profile_form':profile_form})

def signin(request):
    referer = request.META.get('HTTP_REFERER')

    if request.method == 'POST':
        # print(referer)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if "book" in referer:
                    return redirect(request.GET['next'])
                else:
                    return redirect('/azbakya/profile/' + username)
        else:
            form = SignInForm()
            return render(request, 'azbakya/signin.html', {'form': form,'error' : "invalid Username Or Password, Please Check Your Login Data"})
    else:
        form = SignInForm()
    return render(request, 'azbakya/signin.html', {'form': form})

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

def mark_read(request,bookID):
    bookIns = Book.objects.get(pk=bookID)
    record = UserBookRead(book = bookIns,user = request.user)
    record.save()
    data = {}
    return JsonResponse(data)

def already_read(request,bookID):
    bookIns = Book.objects.get(pk=bookID)
    record = UserBookRead.objects.get(book = bookIns,user = request.user)
    record.delete()
    data = {}
    return JsonResponse(data)


def cat_fav(request,categoryID):
    # referer = request.META.get('HTTP_REFERER')
    catIns = Category.objects.get(pk=categoryID)
    if(CategoryUser.objects.filter(category=catIns,user=request.user)):
        record = CategoryUser.objects.get(category=catIns,user=request.user)
        record.delete()
    else:
        record = CategoryUser(category=catIns,user=request.user)
        record.save()
    data = {}
    return JsonResponse(data)

def add_wish(request,bookID):
    bookIns = Book.objects.get(pk=bookID)
    record = UserBookWish(book = bookIns,user = request.user)
    record.save()
    data = {}
    return JsonResponse(data)

def remove_wish(request,bookID):
    bookIns = Book.objects.get(pk=bookID)
    record = UserBookWish.objects.get(book = bookIns,user = request.user)
    record.delete()
    data = {}
    return JsonResponse(data)

def rating(request,bookID):
    # rate = request.GET['rating']
    print(request.body)
    dict1 = json.loads(request.body.decode("utf-8"))
    print(dict1)
    rate = dict1['rating']
    bookIns = Book.objects.get(pk=bookID)
    if(UserBookRate.objects.filter(book=bookIns,user=request.user)):
        record = UserBookRate.objects.get(book=bookIns,user=request.user)
        record.rate = int(rate)
        record.save()
    else:
        record = UserBookRate(book=bookIns,user=request.user,rate=int(rate))
        record.save()
    data = {}
    return JsonResponse(data)
