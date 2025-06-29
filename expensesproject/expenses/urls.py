from django.urls import path
from . import views



urlpatterns = [
    path('',views.index, name="expenses"),
    path('add-expenses',views.add_expense, name="add-expenses"),
    # path('edit-expense/<int:id>',views.expense_edit, name="expense-edit")
    path('edit-expense/<int:id>', views.expense_edit, name="expense_edit"),
    path('expense-delete/<int:id>', views.delete_expense, name="expense-delete")

]
