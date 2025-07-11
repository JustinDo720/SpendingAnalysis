from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .models import Category, Transactions
from .serializers import CategoryReadSerializer, CategoryWriteSerializer, CategoryRetrieveSerializer, TransactionReadSerializer, TransactionWriteSerializer

# Create your views here.

# Creating a homepage view to have all of our links 
@api_view(['GET'])
def home_page(request, format=None):
    return Response({
        # We used category-list because that's the default name of our Viewset 
        'categories': reverse('category-list', request=request, format=format),
        'transactions': reverse('transaction-list-create', request=request, format=format)
    })

class CategoryViewSet(viewsets.ModelViewSet):
    """
        Category View Set for listing, retrieving, creating, updating and detroying our categories
    """
    queryset = Category.objects.all()
    lookup_field = 'slug'

    # Custom Serializer Class 
    def get_serializer_class(self):
        # Checking our action (If it's a POST, PUT, DELETE then we use the Write serializer)
        if self.action in ['create', 'update', 'destroy']:
            return CategoryWriteSerializer
        elif self.action == 'retrieve':
            return CategoryRetrieveSerializer
        return CategoryReadSerializer
    
    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object() 
        serializer = self.get_serializer(instance, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': "Category was removed..."
        }, status=status.HTTP_200_OK)
    

class TransactionSerializerMixin:
    def get_serializer_class(self):
        # Because we are no longer using ViewSets we don't have access to Action so we have self.request.method 
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return TransactionWriteSerializer
        return TransactionReadSerializer

class ListCreateTransactionAPIView(TransactionSerializerMixin, generics.ListCreateAPIView):
    """
        View all Transactions in our Database
        - Create a Transaction if needed
    """
    queryset = Transactions.objects.all()

    def get(self, request):
        """
            Returns all our transactions that exists
        """
        transactions = self.get_queryset()
        serializer = self.get_serializer(transactions, many=True)
        return Response({'all_transactions': serializer.data})

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class TransactionDetailsAPIView(TransactionSerializerMixin, generics.RetrieveUpdateDestroyAPIView):
    """
        Transaction generic API View to Retrieve, Update and Destroy 
        - This API Focuses more on viewing, updating or destroying a specific Transaction 
    """
    queryset = Transactions.objects.all()
    
    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serialzier = self.get_serializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serialzier.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response({'message': 'Transaction was removed'}, status=status.HTTP_200_OK)
    