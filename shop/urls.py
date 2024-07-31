from django.urls import include, path
from shop import views
from .views import BookListView, register

urlpatterns = [
    path('', views.index, name='index'),
    path('books/sort_books/', views.sort_books, name='sort_books'),
    path('books/book_search/', views.book_search, name='book_search'),
    path('books/', BookListView.as_view(), name='books'),
    path('books/<int:pk>', views.BookDetailView.as_view(), name='book_detail'),
    
    path('users/<int:pk>', views.profile.as_view(), name='user_detail'),
    path('users/<int:pk>/edit/', views.edit_profile, name='edit_profile'),
    path('users/cart/', views.Cart, name='cart'),
    path('users/collection/', views.Collection_detail, name='collection'),
    path('users/comment/', views.Comment_detail, name='comment'),
    
    path('orders/', views.order_list, name='order_list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('orders/checkout_sum/', views.checkout_sum, name='checkout_sum'),
    
    path('books/<int:book_id>/checkout/', views.checkout, name='checkout'),
    path('books/<int:book_id>/add_comment/', views.add_comment, name='add_comment'),
    path('books/<int:book_id>/add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('books/<int:book_id>/add_to_favorites/', views.add_to_collection, name='add_to_collection'),
    
    path('users/add_fund/', views.add_fund, name='add_fund'),
    path('users/cart/change_cart/', views.change_cart, name='change_cart'),
    path('users/cart/move_to_collection/<int:cart_id>/', views.move_to_collection, name='move_to_collection'),
    path('users/cart/delete_cart_item/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('users/cart/get_purchase_form/', views.get_purchase_form, name='get_purchase_form'),
    path('users/collection/delete_collection/', views.delete_collection, name='delete_collection'),
    path('users/cart/update_total_price/', views.update_total_price, name='update_total_price'),
]

