from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80, blank=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='books', db_index=True)
    name = models.CharField(max_length=80, blank=True, db_index=True)
    isbn = models.CharField('isbn', max_length=13, unique=True, help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">isbn number</a>')
    author = models.CharField(max_length=80, blank=True, db_index=True)  
    pub_house = models.CharField(max_length=80, blank=True)
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    description = models.TextField(blank=True)
    list_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Book"
        verbose_name_plural = "Books"
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['author']),  
            models.Index(fields=['category']),
        ]


class UserInfo(AbstractUser):
    pay_password = models.CharField(max_length=80, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to='user_images/', blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse('user_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['username']

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_orders')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_orders')
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=6, blank=True)
    tel = models.CharField(max_length=20, blank=True)
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=10, blank=True, choices=[('Pending', 'Pending'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered')])
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

    def get_absolute_url(self):
        return reverse('order_detail', kwargs={'pk': self.id})

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"
        ordering = ['-order_date']

class Comment(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_comments')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_comments')
    text_content = models.CharField(max_length=255, blank=True, null=True)
    comment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.book.name}"

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-comment_date']

class Collection(models.Model):
    id = models.AutoField(primary_key=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_collections')
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_collections')

    def __str__(self):
        return self.book.name

    class Meta:
        verbose_name = "Collection"
        verbose_name_plural = "Collections"
        ordering = ['user', 'book']

class CartItem(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, related_name='user_cart_items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='book_cart_items')
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return self.book.name

    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        ordering = ['user', 'book']
