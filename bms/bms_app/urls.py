from django.urls import path
from .company import CompanyAPIView
from .misc import ItemsAPIView, RemarkAPIView, TaxAPIView, GSTAPIView
from .party import PartyAPIView
from .transaction import TransactionAPIView
from .views import SampleView

urlpatterns = [
    path('', SampleView.as_view(), name='sample-view'),
    path('companies/', CompanyAPIView.as_view(), name='company-list-create'),
    path('companies/<int:company_id>/', CompanyAPIView.as_view(),
         name='company-detail-update-delete'),
    path('parties/', PartyAPIView.as_view(), name='party-list-create'),
    path('parties/<int:party_id>/', PartyAPIView.as_view(),
         name='party-detail-update-delete'),
    path('items/', ItemsAPIView.as_view(), name='item-list-create'),
    path('items/<int:item_id>/', ItemsAPIView.as_view(),
         name='item-detail-update-delete'),
    path('remark/', RemarkAPIView.as_view(), name='remark-list-create'),
    path('remark/<int:remark>/', RemarkAPIView.as_view(),
         name='remark-detail-update-delete'),
    path('tax/', TaxAPIView.as_view(), name='tax-list-create'),
    path('tax/<int:tax_id>/', TaxAPIView.as_view(),
         name='tax-detail-update-delete'),
    path('gst/', GSTAPIView.as_view(), name='gst-list-create'),
    path('gst/<int:gst_id>/', GSTAPIView.as_view(),
         name='gst-detail-update-delete'),
    path('transaction/', TransactionAPIView.as_view(),
         name='transaction-list-create'),
    path('transaction/<int:trnx_id>/', TransactionAPIView.as_view(),
         name='transaction-detail-update-delete'),

]
