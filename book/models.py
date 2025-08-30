from django.db import models
from django.utils.html import format_html

# Create your models here.

BOOK_LEVEL_CHOICES = (
    ('B', 'Basic'),
    ('M', 'Medium'),
    ('A', 'Advanced'),
)

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Category' #ชื่อใหม่

    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = 'Author' 

    def __str__(self):
        return self.name

class Book(models.Model):
    category = models.ForeignKey(Category,null=True,blank=True,on_delete=models.CASCADE) # 1 หมวดหมู่ มีหลายหนังสือ
    author = models.ManyToManyField(Author,blank=True)
    code = models.CharField(max_length=10,unique=True)
    slug = models.SlugField(max_length=200,unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True,blank=True)
    price = models.FloatField(default=0)
    published = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    level = models.CharField(max_length=20,choices=BOOK_LEVEL_CHOICES,null=True,blank=True)
    image = models.FileField(upload_to='upload/',null=True,blank=True)
    class Meta:
        ordering = ['-created']
        verbose_name_plural = 'Book' 

    def show_image(self):
        if self.image: # มีการอัปโหลดภาพไหม
            return format_html('<img src="%s" height="40px" />'% self.image.url)
        return '-'
    show_image.allow_tags = True
    show_image.short_description = 'Image'

    def get_comment_count(self):
        return self.bookcomment_set.count()

    def __str__(self):
        return self.name

class BookComment(models.Model):
    book = models.ForeignKey(Book,on_delete=models.CASCADE) # หนังสือ 1 เล่มมีหลาย comment
    comment = models.CharField(max_length=100)
    rating = models.FloatField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name_plural = 'Book Comment'

    def __str__(self):
        return self.comment