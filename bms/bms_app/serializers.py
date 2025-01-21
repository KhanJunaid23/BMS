from rest_framework import serializers
from .models import Company, CompanyPartyInvoiceDetails, FinancialYear, GSTDetails, Items, Party, Remarks, Tax, Transactions


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = ['item_id', 'item_name']


class RemarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Remarks
        fields = ['remark_id', 'remark']


class TaxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tax
        fields = ['tax_id', 'tax_percentage', 'default_tax', 'description']


class GSTDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = GSTDetails
        fields = ['gst_id', 'company', 'financial_year', 'gst']


class PartySerializer(serializers.ModelSerializer):
    class Meta:
        model = Party
        fields = '__all__'


class CompanyPartyInvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyPartyInvoiceDetails
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class FinancialYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialYear
        fields = ['financial_year_id', 'company',
                  'from_date', 'to_date', 'description', 'status']


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = '__all__'
