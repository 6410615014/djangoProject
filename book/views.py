from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Category, Book
from .forms import BookForm
from slugify import slugify
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def index(request):
    categories = Category.objects.all() # ดึงข้อมูลหมวดหมู่ทั้งหมด
    books = Book.objects.filter(published=True) # ดึงข้อมูลหนังสือที่เผยแพร่

    categ_id = request.GET.get('categoryid')
    if categ_id:
        #ถ้า categoryid มีค่า
        books = books.filter(category_id=categ_id)
    
    pagination = Paginator(books,10)
    page = request.GET.get('page')
    try:
        books = pagination.page(page)
    except PageNotAnInteger:
        books = pagination.page(1)
    except EmptyPage:
        books = pagination.page(pagination.num_pages)

    return render(request, 'book/index.html',{
        'books': books, 
        'categories': categories,
        'categ_id': categ_id
    })

def detail(request, slug):
    book = get_object_or_404(Book, slug=slug)
    return render(request, 'book/detail.html', {
        'book': book
    })

def book_add(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.name)
            book.published = True
            book.save()
            form.save_m2m()
            messages.success(request, 'Save success')
            return HttpResponseRedirect(reverse('book:index', kwargs={}))
        messages.error(request, 'Save failed!')
    return render(request, 'book/add.html', {
        'form': form
    })

from django.views.generic import ListView , DeleteView
class BookListView(ListView):
    model = Book
    template_name = 'book/index.html'
    context_object_name = 'books'
    paginate_by = 5

    def get_queryset(self):
        return Book.objects.filter(published=True)
    
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context.update({'categories': Category.objects.all()})
        return context

class BookDetailView(DeleteView):
    model = Book
    template_name = 'book/detail.html'
    slug_url_kwarg = 'slug'

def cart_add(request, slug):
    book = get_object_or_404(Book, slug=slug)
    cart_items = request.session.get('cart_items') or []

    duplicate = False 

    for  c in cart_items:
        if c.get('name') == book.name:
            c['qty'] = int(c.get('qty') or '1') +1
            duplicate = True # พบสินค้าชิ้นนี้ในตะกร้า
    # ถ้าไม่มีสินค้านี้ในตะกร้า
    if not duplicate:
        cart_items.append({
            'id': book.id ,
            'name': book.name,
            'slug': book.slug,
            'price': book.price,
            'qty': 1
        })
    total_qty = sum(item.get('qty', 0) for item in cart_items)
    request.session['cart_items'] = cart_items
    request.session['cart_qty'] = total_qty
    return HttpResponseRedirect(reverse('book:cart_list'))

def cart_list(request):
    cart_items = request.session.get('cart_items') or []
    total_qty = 0
    for c in cart_items:
        total_qty += c.get('qty')
    request.session['cart_qty'] = total_qty
    return render(request, 'book/cart.html',{
        'cart_items': cart_items,
    })

def cart_delete(request, slug):
    cart_items = request.session.get('cart_items') or []
    for i in range(len(cart_items)):
        if cart_items[i]['slug'] == slug:
            del cart_items[i]
            break
    total_qty = sum(item.get('qty', 0) for item in cart_items)
    request.session['cart_items'] = cart_items
    request.session['cart_qty'] = total_qty
    return HttpResponseRedirect(reverse('book:cart_list'))

def cart_checkout(request):
    subject = 'Test Email'
    body = ''' 
    <p>This is a test email message ja.</p>
    '''
    email = EmailMessage(
        subject=subject,
        body=body,
        from_email='kk4.yinyin4@gmail.com',
        to=['kanokwan.kum4@gmail.com']
    )
    email.content_subtype = 'html'  # เพื่อส่งเป็น HTML
    email.send()

    return HttpResponseRedirect(reverse('book:index'))