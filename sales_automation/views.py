from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product, SaleRecord, Shop, Route
from django.http import JsonResponse
import json

@login_required
def dashboard(request):
    # Fetch Data
    recent_sales = SaleRecord.objects.all().order_by('-date')[:10] # Last 10 sales
    total_sales_count = SaleRecord.objects.count()
    
    context = {
        'recent_sales': recent_sales,
        'total_sales_count': total_sales_count
    }
    return render(request, 'sales_automation/dashboard.html', context)

import json
from django.shortcuts import redirect
from django.contrib import messages
from django.views.decorators.csrf import ensure_csrf_cookie

@login_required
@ensure_csrf_cookie
def add_sale(request):
    if request.method == 'POST':
        try:
            # 1. Get the data from the request
            data = json.loads(request.body)
            shop_id = data.get('shop_id')
            items = data.get('items') # This is a list of {product_id, qty}

            # 2. Validation
            if not shop_id or not items:
                return JsonResponse({'status': 'error', 'message': 'Missing shop or items'}, status=400)

            shop = Shop.objects.get(id=shop_id)

            # 3. Create the Main Sale Record (The Header)
            sale = SaleRecord.objects.create(
                rep=request.user,
                shop=shop,
                total_amount=0 # We will update this after adding items
            )

            # 4. Create the Items and calculate total
            grand_total = 0
            
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                qty = int(item['qty'])
                price = product.unit_price # Fetch current price
                
                # Create the line item
                SaleItem.objects.create(
                    sale_record=sale,
                    product=product,
                    quantity=qty,
                    price_at_sale=price
                )
                grand_total += (price * qty)

            # 5. Update the grand total
            sale.total_amount = grand_total
            sale.save()

            messages.success(request, f"Sale recorded for {shop.name}!")
            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    # --- GET REQUEST (Show the HTML page) ---
    shops = Shop.objects.all()
    products = Product.objects.all()
    
    # We pass products as JSON too so JavaScript can read prices easily
    products_json = list(products.values('id', 'name', 'unit_price')) 
    
    context = {
        'shops': shops,
        'products': products,
        'products_json': json.dumps(products_json, default=str) # Send data to JS
    }
    return render(request, 'sales_automation/add_sale.html', context)