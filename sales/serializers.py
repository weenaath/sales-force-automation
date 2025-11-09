from rest_framework import serializers
from .models import SalesArea, SalesRep, Product, SalesEntry
from django.contrib.auth import get_user_model

User = get_user_model()

class SalesAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesArea
        fields = ['id','name','description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','sku','name','default_unit_price','active']

class UserShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email']

class SalesRepSerializer(serializers.ModelSerializer):
    user = UserShortSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True, source='user')

    class Meta:
        model = SalesRep
        fields = ['id','user','user_id','area','phone']

class SalesEntrySerializer(serializers.ModelSerializer):
    rep = serializers.PrimaryKeyRelatedField(queryset=SalesRep.objects.all())
    area = serializers.PrimaryKeyRelatedField(queryset=SalesArea.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), allow_null=True, required=False)

    class Meta:
        model = SalesEntry
        fields = [
            'id','rep','area','customer_name','product','date','quantity','unit_price',
            'total_amount','invoice_no','payment_method','notes','admin_approved',
            'commission_pct','commission_amount','created_at'
        ]
        read_only_fields = ('total_amount','commission_amount','created_at')
