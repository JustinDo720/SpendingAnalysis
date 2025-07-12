from django.shortcuts import render
from rest_framework import viewsets, status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from .models import Category, Transactions, TransactionUploads
from .serializers import CategoryReadSerializer, CategoryWriteSerializer, CategoryRetrieveSerializer, TransactionReadSerializer, TransactionWriteSerializer, TransactionUploadsSerializer, TransactionDetailsSerializer
import pandas as pd


# Create your views here.

# Creating a homepage view to have all of our links 
@api_view(['GET'])
def home_page(request, format=None):
    return Response({
        # We used category-list because that's the default name of our Viewset 
        'categories': reverse('category-list', request=request, format=format),
        'transactions': reverse('transaction-list-create', request=request, format=format),
        'transactions_upload': reverse('transaction-uploads-list-create', request=request, format=format)
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

class TransactionUploadAPIView(generics.ListCreateAPIView):
    """
        File Uploads to perform data analytics 
    
    """
    queryset = TransactionUploads.objects.all()
    serializer_class = TransactionUploadsSerializer
    # In order for us to work with file uplaods we need a multiparser 
    parser_classes = [MultiPartParser,]

    def get(self, request):
        # Listing All of our Transactions 
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'uploaded_files': serializer.data
        })
    
    def post(self, request):
        # Uploading the file 
        # serializer = self.get_serializer(data=request.data,files=request.FILES)  ## No longer have to use request.FILES in GenericAPIVIews
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save() 
            # Work with pandas???
            file = instance.file
            df = pd.read_csv(file)

            # Normalize/Clean Data (lowercase vendors, making sure amount is float)
            #
            # Assuming we have headers => Date,Vendor,Category,Amount
            df['Vendor'] = df['Vendor'].str.strip()     # Removing White Spaces 
            df['Category'] = df['Category'].str.strip().str.lower()     # Remove White Spaces + Lower because we'll be adding them into Category model
            df['Amount'] = df['Amount'].astype(float)
            # Making sure our date follows the right format 
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')    # coerce just fills in NA if time isn't valid 
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')   # We could use .dt to transform into date time 


            # Create Categories if not exists
            # Insert Transactions 
            transactions_created = 0 
            for index, row in df.iterrows():
                # We could use get_or_create it's simialrt to get_or_404
                # Row is our series 
                category_obj, _ = Category.objects.get_or_create(category_name=row['Category'])
                # Now let's make our Transactions 
                transaction = Transactions.objects.create(
                    vendor=row['Vendor'],
                    amount=row['Amount'],
                    date=row['Date'],
                    # We need to provide the object itself for FK
                    category=category_obj,
                    transaction_upload=instance
                )
                transactions_created += 1

            # Summary 
            # Group by Category, Sum the total, Sort by descing (Largest-Smallest), transform to dict for our resposne
            summary = df.groupby('Category')['Amount'].sum().sort_values(ascending=False).to_dict()
            return Response({
                'message': f"{transactions_created} number of Transactions were created from your uploaded file.",
                'upload_id': instance.id,
                'spending_summary': summary
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TransactionUploadDetailsAPIView(generics.RetrieveDestroyAPIView):
    """
        API View to Retrieve or Destroy
        - When we destroy this file... we remove all the related transactions 
        - We don't to want update because it'll mess with the transactions 
    """
    queryset = TransactionUploads
    serializer_class = TransactionDetailsSerializer
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def delete(self, request):
        instance = self.get_object()
        instance.delete()
        return Response({
            'message': "Upload file and all related transactions were removed from our system..."
        })
    
# Summary (Actionable & Meaningful Insights)
class TransactionSummaryAPIView(APIView):
    """
        Returns Actionable & Meaningful Data based on all the transaction related to our file 
    """

    def get(self, request, upload_id):
        # Prefetch transactions for one bulky query instead of opening the DB again and again
        upload = TransactionUploads.objects.prefetch_related('transactions').get(id=upload_id)
        # Now when we do upload.transactions.all() we don't open the DB again since its prefetchedc
        related_transactions = upload.transactions.all()

        # Rebuilding Data for Dataframe 
        data = [{
            'vendor': t.vendor,
            'amount': float(t.amount),
            'date': t.date,
            'category': t.category.category_name
        } for t in related_transactions]

        df = pd.DataFrame(data)

        # Meaningful Insights
        total_spent = round(df['amount'].sum(),2)
        spending_per_category = df.groupby('category')['amount'].sum().sort_values(ascending=False).to_dict()
        # We could use head(n) to grab n rows (Since its already sorted the top will be the most spent)
        top_vendors = df.groupby('vendor')['amount'].sum().sort_values(ascending=False).head(5).to_dict()

        return Response({
            'total_spent': total_spent,
            'spending_per_category': spending_per_category,
            'top_vendors': top_vendors
        })