from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from utilisateurs.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from store.utils import cartData

def login_view(request):
    data = cartData(request)
    cartItems = data['cartItems']

    user = request.user
    if user.is_authenticated: 
        return redirect("home")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("home")

    else:
        form = AccountAuthenticationForm()

    context = {'cartItems':cartItems,"login_form":form}
    return render(request, "utilisateurs/login.html", context)

def register_user(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("/login/")
        else:
            context = {'cartItems':cartItems,"registration_form":form}

    else:
        form = RegistrationForm()
        context = {'cartItems':cartItems,"registration_form":form}
    return render(request, 'utilisateurs/register.html', context)

def register_seller(request):
    data = cartData(request)
    cartItems = data['cartItems']

    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect("/login/")
        else:
            context = {'cartItems':cartItems,"registration_form":form}

    else:
        form = RegistrationForm()
        context = {'cartItems':cartItems,"registration_form":form}
    return render(request, 'utilisateurs/registerAsSeller.html', context)

def account_view(request):
    # data = cartData(request)
    # cartItems = data['cartItems']

    if not request.user.is_authenticated:
            return redirect("login")

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
            }
            form.save()
            # context = {'cartItems':cartItems,"success_message":"Updated"}
            context = {"success_message":"Updated"}
    else:
        form = AccountUpdateForm(

            initial={
                    "email": request.user.email, 
                    "username": request.user.username,
                }
            )

    # context = {'cartItems':cartItems,"account_form":form}
    context = {"account_form":form}

    # blog_posts = BlogPost.objects.filter(author=request.user)
    # context['blog_posts'] = blog_posts

    return render(request, "store/account.html", context)

# def must_authenticate_view(request):
# 	return render(request, 'account/must_authenticate.html', {})
