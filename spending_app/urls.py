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
    path('transactions/<int:pk>/', views.TransactionDetailsAPIView.as_view(), name='transactions-detail')
]
