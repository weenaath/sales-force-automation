from datetime import date
from django.db.models import Sum, F 
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SaleRecord, Shop, Route, SaleItem, Product
from django.http import JsonResponse
import json

@login_required
@login_required
def dashboard(request):
    # --- SCENARIO 1: ADMIN ---
    if request.user.is_superuser:
        # --- 1. KPI CARDS ---
        recent_sales = SaleRecord.objects.all().order_by('-date')[:10]
        total_sales_count = SaleRecord.objects.count()
        total_revenue = SaleRecord.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # --- 2. CHART: SALES TREND (Area Chart) ---
        # Get sales for the last 30 days
        last_30_days = datetime.date.today() - datetime.timedelta(days=30)
        daily_sales = SaleRecord.objects.filter(date__gte=last_30_days)\
            .extra(select={'day': 'date(date)'})\
            .values('day')\
            .annotate(total=Sum('total_amount'))\
            .order_by('day')
        
        trend_labels = [item['day'] for item in daily_sales]
        trend_data = [float(item['total']) for item in daily_sales]

        # --- 3. CHART: REP PERFORMANCE (Bar Chart) ---
        rep_performance = SaleRecord.objects.values('rep__username').annotate(
            total=Sum('total_amount')
        ).order_by('-total')[:5]

        rep_labels = [item['rep__username'] for item in rep_performance]
        rep_data = [float(item['total']) for item in rep_performance]

        # --- 4. EXISTING CHARTS ---
        # Top Products
        sales_by_product = SaleItem.objects.values('product__name').annotate(
            revenue=Sum(F('quantity') * F('price_at_sale'))
        ).order_by('-revenue')[:5]
        product_labels = [item['product__name'] for item in sales_by_product]
        product_data = [float(item['revenue']) for item in sales_by_product]

        # Sales by Route
        sales_by_route = SaleRecord.objects.values('shop__route__name').annotate(
            total=Sum('total_amount')
        ).order_by('-total')
        route_labels = [item['shop__route__name'] for item in sales_by_route]
        route_data = [float(item['total']) for item in sales_by_route]

        context = {
            'recent_sales': recent_sales,
            'total_sales_count': total_sales_count,
            'total_revenue': total_revenue,
            # JSON Data for JS
            'trend_labels': json.dumps(trend_labels, default=str),
            'trend_data': json.dumps(trend_data),
            'rep_labels': json.dumps(rep_labels),
            'rep_data': json.dumps(rep_data),
            'product_labels': json.dumps(product_labels),
            'product_data': json.dumps(product_data),
            'route_labels': json.dumps(route_labels),
            'route_data': json.dumps(route_data),
        }
        return render(request, 'sales_automation/dashboard_admin.html', context)

    # --- SCENARIO 2: SALES REP (The User) ---
    else:
        # 1. Personal Data Only (Filter by rep=request.user)
        my_sales = SaleRecord.objects.filter(rep=request.user).order_by('-date')
        
        # Calculate stats
        today = date.today()
        sales_today = my_sales.filter(date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_my_sales = my_sales.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        visit_count = my_sales.count()

        context = {
            'recent_sales': my_sales[:10], # Last 10 personal sales
            'sales_today': sales_today,
            'total_my_sales': total_my_sales,
            'visit_count': visit_count
        }
        return render(request, 'sales_automation/dashboard_rep.html', context)

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