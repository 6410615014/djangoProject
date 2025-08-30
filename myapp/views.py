from email.message import EmailMessage
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , logout
from django.urls import reverse

# Create your views here.
def index(request):
    id = '001'
    name = 'aomnaiiii'
    email = 'aomnaiiii@example.com'
    activities = ['Football', 'Running', 'Badminton']
    return render(request, 'index.html',{
        'id' : id,
        'name' : name ,
        'email' : email,
        'activities' : activities
    })

def hello(request,id):
    greeting = 'Your ID: {0}'.format(id)
    return HttpResponse(greeting)

def article(request, year, slug):
    return HttpResponse('Article year='+str(year)+', slug='+slug)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book:index') 
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('myapp:index')
    
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book:index')
    else:
        form = UserCreationForm()
    return render(request, 'account/signup.html', {'form': form})

def cart_checkout(request):
    subject = 'Your Cart Checkout'
    body = ''' 
    <p>Thank you for your purchase!</p>
    '''
    email = EmailMessage(subject=subject, body=body, from_email='kk4.yinyin4@gmail.com', to=['kanokwan.kum4@gmail.com'])
    email.content_subtype = 'html'
    email.send()

    return HttpResponseRedirect(reverse('book:index'))