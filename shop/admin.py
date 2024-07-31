from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Book, UserInfo, Order, Comment, Collection, CartItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'category', 'list_price', 'quantity', 'display_image')
    search_fields = ('name', 'author', 'isbn')
    list_filter = ('category__name',)
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Book Image'

@admin.register(UserInfo)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_staff', 'date_joined')
    search_fields = ('username', 'email')
    list_filter = ('is_staff',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'order_date', 'status')
    search_fields = ('user__username', 'status')
    list_filter = ('status', 'order_date')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user', 'text_content', 'comment_date')
    search_fields = ('text_content', 'user__username')
    list_filter = ('book__name', 'user__username')

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'book', 'user')
    search_fields = ('book__name', 'user__username')
    list_filter = ('user__username',)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'book', 'quantity')
    search_fields = ('book__name', 'user__username')
    list_filter = ('user__username',)
