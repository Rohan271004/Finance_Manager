from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Expense
from django.contrib import messages

# Create your views here.

@login_required(login_url='/authentication/login')
def index(request):
    Categories = Category.objects.all()
    expenses = Expense.objects.filter(owner=request.user)
    
    context={
        'expenses':expenses
    }
    return render(request, 'expenses/index.html',context)


@login_required(login_url='/authentication/login')  
def add_expense(request):
    Categories = Category.objects.all()

    context = {
            'categories' : Categories,
            'values': request.POST
        }
    if request.method == 'GET':

        return render(request, 'expenses/add_expense.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        if not amount:
            messages.error(request,"Amount is required")
            return render(request, 'expenses/add_expense.html', context)
    
        description = request.POST['description']
        date = request.POST['expense-date']
        category = request.POST['category']


        if not description:
            messages.error(request,"Description is required")
            return render(request, 'expenses/add_expense.html', context)

        Expense.objects.create(owner=request.user,amount=amount,date=date,category=category,description=description)
        messages.success(request,'Expense saved successfully')

        return redirect('expenses')
    
def expense_edit(request,id):
    Categories = Category.objects.all()
    expense = Expense.objects.get(pk=id)
    context = {
        'categories' : Categories,
        'expense': expense,
        'values' : expense
    }
    if request.method == 'GET':
        
        return render(request, 'expenses/edit-expense.html',context)
    if request.method == 'POST':

        amount = request.POST['amount']

        if not amount:
            messages.error(request,"Amount is required")
            return render(request, 'expenses/edit-expense.html', context)
    
        description = request.POST['description']
        date = request.POST['expense-date']
        category = request.POST['category']


        if not description:
            messages.error(request,"Description is required")
            return render(request, 'expenses/edit-expense.html', context)

        
        expense.owner = request.user
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.category = category

        expense.save()
        messages.success(request,'Expense updated successfully')

        return redirect('expenses')

def delete_expense(request, id):
    expense = Expense.objects.get(pk=id)
    expense.delete()
    messages.success(request, "Expense removed")
    return redirect('expenses')