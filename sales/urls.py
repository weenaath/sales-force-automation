from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesAreaViewSet, ProductViewSet, SalesRepViewSet, SalesEntryViewSet

router = DefaultRouter()
router.register('areas', SalesAreaViewSet)
router.register('products', ProductViewSet)
router.register('reps', SalesRepViewSet)
router.register('sales', SalesEntryViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
