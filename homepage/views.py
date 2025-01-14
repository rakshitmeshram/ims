from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import View, TemplateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login 
from inventory.models import Stock
from transactions.models import SaleBill, PurchaseBill
from .forms import RegisterForm

def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()
    return render(response, "register/register.html", {"form": form})

# class SignUpForm(View):
#     def get(self, request):
#         form = UserCreationForm()
#         return render(request, 'signup.html', {'form': form})
    
#     def post(self, request):
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#         else:
#             form = UserCreationForm()
#         return render(request, 'signup.html', {'form': form})

@login_required
def home(response):
    template_name = "home.html"
    if response.method == "GET":        
        labels = []
        data = []        
        stockqueryset = Stock.objects.filter(is_deleted=False).order_by('-quantity')
        for item in stockqueryset:
            labels.append(item.name)
            data.append(item.quantity)
        sales = SaleBill.objects.order_by('-time')[:3]
        purchases = PurchaseBill.objects.order_by('-time')[:3]
        context = {
            'labels'    : labels,
            'data'      : data,
            'sales'     : sales,
            'purchases' : purchases
        }
    return render(response, template_name, context)


class AboutView(TemplateView):
    template_name = "about.html"


