from django.db import models
from django.db.models.fields.files import ImageField
from django.contrib.auth.models import User

# User = get_user_model()

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author',on_delete=models.CASCADE)
    publish = models.DateField('date of publish',null=True,blank=True)
    summary = models.TextField(null=True,blank=True)
    image = models.ImageField( upload_to='media/books',null=True,blank=True)
    user = models.ManyToManyField(User,through='UserBookRead')
    user = models.ManyToManyField(User,through='UserBookWish')
    user = models.ManyToManyField(User,through='UserBookRate')
    def __str__(self):
        return self.title


class Author(models.Model):
    name = models.CharField(max_length=200)
    dob = models.DateField('date of birth',null=True,blank=True)
    bio = models.TextField('biography',null=True,blank=True)
    image = models.ImageField( upload_to='media/authors',null=True,blank=True)
    user = models.ManyToManyField(User,through='UserAuthor')
    def __str__(self):
    	return self.name
    def filterI(self,num):
        return self.user.get(pk=num)


class Category(models.Model):
    name = models.CharField(max_length=200)
    book = models.ManyToManyField('Book',through='CategoryBook')
    user = models.ManyToManyField(User,through='CategoryUser')
    def __str__(self):
    	return self.name


class UserBookRead(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user","book",)

class UserBookWish(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user","book",)

class UserBookRate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    rate = models.PositiveSmallIntegerField(default=0)
    class Meta:
        unique_together = ("user","book",)

class CategoryUser(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user","category",)

class UserAuthor(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    author = models.ForeignKey('Author',on_delete=models.CASCADE)
    class Meta:
        unique_together = ("user","author",)

class CategoryBook(models.Model):
    category = models.ForeignKey('Category',on_delete=models.CASCADE)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    class Meta:
        unique_together = ("book","category",)

class profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    image = models.ImageField( upload_to='media/users')
    class Meta:
        unique_together = ("user","image",)
    def __str__(self):
        return str(self.user.username)
