from rest_framework import viewsets, permissions, filters
from .models import SalesArea, Product, SalesRep, SalesEntry
from .serializers import (
    SalesAreaSerializer, ProductSerializer,
    SalesRepSerializer, SalesEntrySerializer
)

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class SalesAreaViewSet(viewsets.ModelViewSet):
    queryset = SalesArea.objects.all()
    serializer_class = SalesAreaSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

class SalesRepViewSet(viewsets.ModelViewSet):
    queryset = SalesRep.objects.select_related('user','area').all()
    serializer_class = SalesRepSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

class SalesEntryViewSet(viewsets.ModelViewSet):
    queryset = SalesEntry.objects.select_related('rep','area','product').all()
    serializer_class = SalesEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['rep__user__username','invoice_no','customer_name']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        # if user is a sales rep, limit to their entries
        try:
            rep = user.sales_rep
            if not user.is_staff:  # non-admin reps see only their sales
                return qs.filter(rep=rep)
        except Exception:
            pass
        # admins see all
        return qs
