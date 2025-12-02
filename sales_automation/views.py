from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import SaleRecord, Shop, Route

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