from django.shortcuts import render

def checkout(request):
    return render(request, 'orders/checkout.html', {'custom_page_title': 'Checkout' })

"""
fields for Order:

- first name, last name
- phone
- email
- address, drop off location? station?
- delivery option
= requested delivery date

- total price

Settings:
- delivery charge
- email to, email from? or keep in settings via env vars?

"""