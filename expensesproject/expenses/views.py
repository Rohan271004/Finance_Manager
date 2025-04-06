from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    Categories = Category.objects.all()
    return render(request, 'expenses/index.html')

@login_required(login_url='/authentication/login')  
def add_expense(request):
    Categories = Category.objects.all()
    context = {
        'categories' : Categories
    }
    
    return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

    if not amount:
        messages.error(request,"Amount is required")
        return render(request, 'expenses/add_expenses.html', context)