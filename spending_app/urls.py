from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    # Make sure our Home Page API goes first to show all the urls
    path('', views.home_page, name='home-page'),
    path('', include(router.urls)),
    # Transactions
    path('transactions/', views.ListCreateTransactionAPIView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', views.TransactionDetailsAPIView.as_view(), name='transactions-detail'),
    # Upload CSV Transactions 
    path('uploads/', views.TransactionUploadAPIView.as_view(), name='transaction-uploads-list-create'),
    path('uploads/<int:id>/', views.TransactionUploadDetailsAPIView.as_view(), name='transaction-uploads-detail'),
    # Summary 
    path('uploads/<int:upload_id>/summary/', views.TransactionSummaryAPIView.as_view(), name='summary-transaction-uploads'),
    path('uploads/<int:upload_id>/summary/download/', views.TransactionPDFView.as_view(), name='summary-transaction-uploads-download')
]
