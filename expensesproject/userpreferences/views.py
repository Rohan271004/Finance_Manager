from django.shortcuts import render, redirect
import os
import json
from django.conf import settings
from .models import Userpreferences
from django.contrib import messages

def index(request):
    currency_data = []

    file_path = os.path.join(settings.BASE_DIR, 'currencies.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        for k, v in data.items():
            currency_data.append({
                'name': k,
                'value': v
            })

    user_preferences = Userpreferences.objects.filter(user=request.user).first()

    if request.method == 'GET':
        selected_currency = user_preferences.currency if user_preferences else 'INR'  # Default to INR
        return render(request, 'preferences/index.html', {
            'currencies': currency_data,
            'selected_currency': selected_currency
    })


    if request.method == 'POST':
        currency = request.POST.get('currency')

        if user_preferences:
            user_preferences.currency = currency
            user_preferences.save()
        else:
            Userpreferences.objects.create(user=request.user, currency=currency)

        messages.success(request, 'Changes Saved')
        return redirect('preferences')
