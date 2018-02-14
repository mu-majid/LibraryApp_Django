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
        print(referer)
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
    else:
        form = SignInForm()
    return render(request, 'azbakya/signin.html', {'form': form})

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

