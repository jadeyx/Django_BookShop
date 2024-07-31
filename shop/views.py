from decimal import Decimal
from django.utils import timezone
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from shop.models import Book, CartItem, Order, UserInfo, Collection, Comment
from .forms import CartOrderForm, CustomUserCreationForm, PurChaseForm, UserProfileForm
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login, authenticate
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import asyncio
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    book_list = Book.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(book_list, 24)  
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'books': books})

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
            else:
                print("Authentication failed for user:", username)
        else:
            print("Form is not valid:", form.errors)
            return render(request, 'registration/register.html', {'form': form, 'errors': form.errors})
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

class profile(generic.DetailView):
    model = UserInfo
    context_object_name = 'user'
    template_name = 'users/profile.html'


class BookListView(generic.ListView):
    model = Book
    context_object_name = 'book_list'   
    queryset = Book.objects.all()
    template_name = 'books/book_list.html' 
    
class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'books/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(book=self.object)
        context['form'] = PurChaseForm()
        return context

@login_required
def Cart(request):
    model = CartItem
    context_object_name = 'cart_item'
    template_name = 'users/cart.html'
    user_cart_items = model.objects.filter(user=request.user)
    
    context = {
        context_object_name: user_cart_items
    }
    return render(request, template_name, context)

@login_required
def Collection_detail(request):
    model = Collection
    context_object_name = 'collection_item'
    template_name = 'users/collection.html'
    user_collection = model.objects.filter(user=request.user)
    
    context = {
        context_object_name: user_collection
    }
    return render(request, template_name, context)

@login_required
def Comment_detail(request):
    model = Comment
    context_object_name = 'comment_item'
    template_name = 'users/comment.html'
    user_comment = model.objects.filter(user=request.user)
    
    context = {
        context_object_name: user_comment
    }
    return render(request, template_name, context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    

@login_required
def add_comment(request, book_id):
    if request.method == 'POST':
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        
        comment = Comment.objects.create(
            book=book,
            user=user,
            text_content=request.POST.get('text_content', ''),
            comment_date=timezone.now()
        )
        
        comment.save()
        return redirect('book_detail', pk=book_id)

@login_required
def add_to_cart(request, book_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        
        cart_item, created = CartItem.objects.get_or_create(
            user=user,
            book=book,
            defaults={'quantity': 1}
        )
        
        if not created:
            cart_item.quantity += 1
            cart_item.save()
        
        return JsonResponse({'status': 'success', 'message': 'Item added to cart successfully'})
    else:
        return redirect('book_detail', pk=book_id)

@require_POST
def delete_cart_item(request, cart_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        if cart_id:
            try:
                cart_item = CartItem.objects.get(id=cart_id)
                cart_item.delete()
                return JsonResponse({'status': 'success', 'message': '购物车项已删除'})
            except CartItem.DoesNotExist:
                return JsonResponse({'status': 'error', 'message': '购物车项不存在'})
        else:
            return JsonResponse({'status': 'error', 'message': '缺少 cart_id 参数'})



@login_required
def change_cart(request):
    if request.method == 'POST':
        cart_ids = request.POST.getlist('cart_ids')
        move_to_collection = request.POST.get('move_to_collection', 'false') == 'true'

        if move_to_collection:
            cart_items = CartItem.objects.filter(id__in=cart_ids)
            for cart_item in cart_items:
                Collection.objects.get_or_create(user=request.user, book=cart_item.book)
            cart_items.delete()
        else:
            CartItem.objects.filter(id__in=cart_ids).delete()
        return redirect('cart')


@login_required
def add_to_collection(request, book_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
        book = get_object_or_404(Book, id=book_id)
        
        collection, created = Collection.objects.get_or_create(
            user=user,
            book=book,
        )
        
        if created:
            return JsonResponse({'status': 'success', 'message': 'Item added to collection successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Item already in collection'})
    else:
        return redirect('book_detail', pk=book_id)

@login_required
def move_to_collection(request, cart_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            cart_item = get_object_or_404(CartItem, id=cart_id, user=request.user)
            book = cart_item.book
            
            collection, created = Collection.objects.get_or_create(
                user=request.user,
                book=book,
            )
            
            if created:
                cart_item.delete()
                return JsonResponse({'status': 'success', 'message': 'Item moved to collection successfully'})
            else:
                return JsonResponse({'status': 'error', 'message': 'Item already in collection'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return redirect('cart')

@login_required
def delete_collection(request):
    if request.method == 'POST':
        collection_ids = request.POST.getlist('collection_ids')
        Collection.objects.filter(id__in=collection_ids).delete()
        return redirect('collection')



@login_required
def delete_order(request):
    if request.method == 'POST':
        order_ids = request.POST.getlist('order_ids')
        Order.objects.filter(id__in=order_ids).delete()
        return redirect('order_list')
    
def book_search(request):
    search_text = request.GET.get('search_text', '')

    if request.method == 'POST':
        search_text = request.POST.get('search_text', '')

    books = Book.objects.filter(
        Q(name__icontains=search_text) | 
        Q(author__icontains=search_text) | 
        Q(category__name__icontains=search_text)
    )
    paginator = Paginator(books, 24)  
    page = request.GET.get('page', 1)

    try:
        books_paginated = paginator.page(page)
    except PageNotAnInteger:
        books_paginated = paginator.page(1)
    except EmptyPage:
        books_paginated = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'books': books_paginated, 'search_text': search_text})

def edit_profile(request, pk):
    profile = get_object_or_404(UserInfo, pk=pk)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_detail', pk=pk)
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'users/edit_profile.html', {'form': form, 'user': profile})

def sort_books(request):
    sort_by = request.GET.get('sort', None)
    search_text = request.GET.get('search_text', '')
    sort_order = request.GET.get('order', 'asc')  

    if sort_by == 'price':
        if sort_order == 'asc':
            books = Book.objects.all().order_by('list_price')
        else:
            books = Book.objects.all().order_by('-list_price')
    elif sort_by == 'comments':
        if sort_order == 'asc':
            books = Book.objects.annotate(comment_count=Count('book_comments')).order_by('comment_count')
        else:
            books = Book.objects.annotate(comment_count=Count('book_comments')).order_by('-comment_count')
    else:
        books = Book.objects.all()

    if search_text:
        books = books.filter(Q(name__icontains=search_text) | Q(author__icontains=search_text) | Q(category__name__icontains=search_text))

    paginator = Paginator(books, 24)
    page = request.GET.get('page', 1)

    try:
        books_paginated = paginator.page(page)
    except PageNotAnInteger:
        books_paginated = paginator.page(1)
    except EmptyPage:
        books_paginated = paginator.page(paginator.num_pages)

    context = {
        'books': books_paginated,
        'sort': sort_by,
        'search_text': search_text,
        'sort_order': sort_order, 
    }

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render(request, 'books/book_search_results.html', context)
    else:
        return render(request, 'index.html', context)




@require_POST
def update_total_price(request):
    cart_item_ids = request.POST.getlist('cart_ids[]')
    total_price = 0
    for cart_item_id in cart_item_ids:
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        total_price += cart_item.book.list_price * cart_item.quantity
    return JsonResponse({'total_price': total_price})

@login_required
@require_POST
def checkout(request, book_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        user = request.user
        quantity = int(request.POST.get('quantity', 1))
        address = request.POST.get('address', '')
        zip_code = request.POST.get('zip_code', '')
        tel = request.POST.get('tel', '')

        book = get_object_or_404(Book, id=book_id)

        total_price = book.list_price * quantity

        if user.amount < total_price:
            return JsonResponse({'status': 'error', 'message': '余额不足'})

        order = Order.objects.create(
            user=user,
            book=book,
            quantity=quantity,
            total_price=total_price,  
            address=address,
            zip_code=zip_code,
            tel=tel,
            status='Pending'
        )

        user.amount -= total_price
        user.save()

        return JsonResponse({'status': 'success', 'message': '购买成功', 'order_id': order.id})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@require_POST
def get_purchase_form(request):
    if request.method == 'POST':
        cart_ids = request.POST.getlist('cart_ids')
        form = CartOrderForm()
        context = {
            'form': form,
            'cart_ids': cart_ids,
        }
        html = render_to_string('orders/purchase_form.html', context, request=request)
        return JsonResponse({'form': html})
    return JsonResponse({'error': 'Invalid request'}, status=400)


@require_POST
def checkout_sum(request):
    form = CartOrderForm(request.POST)
    if form.is_valid():
        address = form.cleaned_data['address']
        zip_code = form.cleaned_data['zip_code']
        tel = form.cleaned_data['tel']

        user = request.user

        cart_ids = form.cleaned_data['cart_ids']

        if not cart_ids:
            return redirect('cart')

        cart_items = CartItem.objects.filter(id__in=cart_ids)

        total_price = sum(cart_item.book.list_price * cart_item.quantity for cart_item in cart_items)

        if user.amount < total_price:
            return redirect('add_fund')

        for cart_item in cart_items:
            Order.objects.create(
                user=user,
                book=cart_item.book,
                address=address,
                zip_code=zip_code,
                tel=tel,
                quantity=cart_item.quantity,
                total_price=cart_item.book.list_price * cart_item.quantity,
                status='Pending'
            )
        user.amount -= total_price
        user.save()
        cart_items.delete()
        return redirect('cart')
    return redirect('cart')

@login_required
def add_fund(request):
    user = request.user
    user.amount += Decimal('1000.00')
    user.save()
    return redirect('user_detail', pk=user.id)
    