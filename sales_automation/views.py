import json
import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .models import SaleRecord, Shop, Route, SaleItem, Product, RepProfile
from django.template.loader import get_template
from xhtml2pdf import pisa

@login_required
def dashboard(request):
    # --- SCENARIO 1: ADMIN (HQ) ---
    if request.user.is_superuser:
        # 1. KPI Cards
        recent_sales = SaleRecord.objects.all().order_by('-date')[:10]
        total_sales_count = SaleRecord.objects.count()
        total_revenue = SaleRecord.objects.aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        # 2. CHART: SALES TREND (Last 30 Days)
        last_30_days = datetime.date.today() - datetime.timedelta(days=30)
        daily_sales = SaleRecord.objects.filter(date__gte=last_30_days)\
            .extra(select={'day': 'date(date)'})\
            .values('day')\
            .annotate(total=Sum('total_amount'))\
            .order_by('day')
        
        trend_labels = [item['day'] for item in daily_sales]
        trend_data = [float(item['total']) for item in daily_sales]

        # 3. CHART: TOP PRODUCTS
        sales_by_product = SaleItem.objects.values('product__name').annotate(
            revenue=Sum(F('quantity') * F('price_at_sale'))
        ).order_by('-revenue')[:5]
        product_labels = [item['product__name'] for item in sales_by_product]
        product_data = [float(item['revenue']) for item in sales_by_product]

        # 4. CHART: SALES BY ROUTE
        sales_by_route = SaleRecord.objects.values('shop__route__name').annotate(
            total=Sum('total_amount')
        ).order_by('-total')
        route_labels = [item['shop__route__name'] for item in sales_by_route]
        route_data = [float(item['total']) for item in sales_by_route]

        # 5. CHART: REP REVENUE (Simple Bar)
        rep_performance = SaleRecord.objects.values('rep__username').annotate(
            total=Sum('total_amount')
        ).order_by('-total')[:5]
        rep_labels = [item['rep__username'] for item in rep_performance]
        rep_data = [float(item['total']) for item in rep_performance]

        # 6. REP TARGET MONITOR (New Real-Time Logic)
        today = datetime.date.today()
        rep_stats = []
        profiles = RepProfile.objects.all() # Get all reps with targets

        for profile in profiles:
            # Calculate sales for THIS MONTH only
            month_sales = SaleRecord.objects.filter(
                rep=profile.user,
                date__year=today.year, 
                date__month=today.month
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
            
            target = profile.monthly_target
            percentage = (month_sales / target * 100) if target > 0 else 0
            
            rep_stats.append({
                'name': profile.user.username,
                'target': target,
                'actual': month_sales,
                'percentage': min(round(percentage), 100)
            })

        context = {
            'recent_sales': recent_sales,
            'total_sales_count': total_sales_count,
            'total_revenue': total_revenue,
            'rep_stats': rep_stats, # <--- Passing the new list to HTML
            # JSON Data
            'trend_labels': json.dumps(trend_labels, default=str),
            'trend_data': json.dumps(trend_data),
            'product_labels': json.dumps(product_labels),
            'product_data': json.dumps(product_data),
            'route_labels': json.dumps(route_labels),
            'route_data': json.dumps(route_data),
            'rep_labels': json.dumps(rep_labels),
            'rep_data': json.dumps(rep_data),
        }
        return render(request, 'sales_automation/dashboard_admin.html', context)

    # --- SCENARIO 2: SALES REP (Field) ---
    else:
        my_sales = SaleRecord.objects.filter(rep=request.user).order_by('-date')
        today = datetime.date.today()
        visit_count = my_sales.count()
        sales_today = my_sales.filter(date__date=today).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        current_month_sales = my_sales.filter(
            date__year=today.year, 
            date__month=today.month
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0

        try:
            profile = RepProfile.objects.get(user=request.user)
            target = profile.monthly_target
        except RepProfile.DoesNotExist:
            target = 100000

        percentage = (current_month_sales / target * 100) if target > 0 else 0

        context = {
            'recent_sales': my_sales[:10],
            'sales_today': sales_today,
            'visit_count': visit_count,
            'monthly_target': target,
            'current_month_sales': current_month_sales,
            'target_percentage': min(round(percentage), 100)
        }
        return render(request, 'sales_automation/dashboard_rep.html', context)

# ... (keep add_sale view as is) ...
@login_required
@ensure_csrf_cookie
def add_sale(request):
    # Copy your existing add_sale code here, no changes needed
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            shop_id = data.get('shop_id')
            items = data.get('items')
            
            # 1. GET GPS DATA FROM REQUEST
            lat = data.get('lat') 
            lon = data.get('lon')

            if not shop_id or not items:
                return JsonResponse({'status': 'error', 'message': 'Missing shop or items'}, status=400)

            shop = Shop.objects.get(id=shop_id)

            # 2. SAVE GPS TO DATABASE
            sale = SaleRecord.objects.create(
                rep=request.user,
                shop=shop,
                total_amount=0,
                gps_lat=lat, # <--- Saving here
                gps_lon=lon  # <--- Saving here
            )

            grand_total = 0
            
            for item in items:
                product = Product.objects.get(id=item['product_id'])
                qty = int(item['qty'])
                price = product.unit_price
                
                SaleItem.objects.create(
                    sale_record=sale,
                    product=product,
                    quantity=qty,
                    price_at_sale=price
                )
                grand_total += (price * qty)

            sale.total_amount = grand_total
            sale.save()

            return JsonResponse({'status': 'success'})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    shops = Shop.objects.all()
    products = Product.objects.all()
    products_json = list(products.values('id', 'name', 'unit_price')) 
    
    context = {
        'shops': shops,
        'products': products,
        'products_json': json.dumps(products_json, default=str)
    }
    return render(request, 'sales_automation/add_sale.html', context)

@login_required
def download_invoice(request, sale_id):
    # 1. Get the sale record
    sale = SaleRecord.objects.get(id=sale_id)
    items = sale.items.all() # Get all products in this sale

    # 2. Render the HTML template with data
    template_path = 'sales_automation/invoice.html'
    context = {'sale': sale, 'items': items}
    template = get_template(template_path)
    html = template.render(context)

    # 3. Create PDF
    response = HttpResponse(content_type='application/pdf')
    # Set filename: "invoice_0005.pdf"
    response['Content-Disposition'] = f'attachment; filename="invoice_{sale.id}.pdf"'
    
    # 4. Convert HTML to PDF
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response