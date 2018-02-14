from django.contrib import admin
from .models import *

admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(UserBookRead)
admin.site.register(UserBookWish)
admin.site.register(UserBookRate)
admin.site.register(CategoryUser)
admin.site.register(CategoryBook)
admin.site.register(UserAuthor)
admin.site.register(profile)
