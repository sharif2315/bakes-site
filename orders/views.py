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
- delivery charge - £5 ??? settings page for admin to set this?

- total price
"""