from rest_framework import serializers
from .models import Category, Transactions, TransactionUploads
from rest_framework.reverse import reverse


# GET method
class TransactionReadSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.SerializerMethodField()
    upload_id = serializers.SerializerMethodField()

    def get_category_name(self, transaction):
        return transaction.category.category_name
    
    def get_upload_id(self, transaction):
        return transaction.transaction_upload.id

    class Meta: 
        model = Transactions
        fields = (
            'id',
            'vendor',
            'amount',
            'date',
            'category_name',
            'category',
            'upload_id',
            'transaction_upload',
            'url',
        )
        extra_kwargs = {
            # Slug Belongs to Category Model make sure the lookup_field belongs to the respective Model NOT THE CURRENT MODEL (Transactions)
            'category': {'view_name': 'category-detail', 'lookup_field': 'slug'},
            'transaction_upload': {'view_name': 'transaction-uploads-detail', 'lookup_field': 'id'}
        }

class NestedTransactionSerializer(serializers.HyperlinkedModelSerializer):
    # Limiting the important information for Nested Transactions Serializer
    class Meta: 
        model = Transactions
        fields = (
            'id',
            'vendor',
            'amount',
            'date',
            'url'
        )

# Put, Patch, Post
class TransactionWriteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transactions
        fields = (
            'vendor',
            'amount',
            'date',
            'category'
        )

# GET method
class CategoryReadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta: 
        model = Category
        fields = (
            'category_name',
            'slug',
            'url'
        )
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'slug'}
        }

class CategoryRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    # Includes all of the transactions for when we view the individual Category
    #
    # Note: This follows the related_name in models
    transactions = NestedTransactionSerializer(many=True, read_only=True)
    class Meta: 
        model = Category
        fields = (
            'category_name',
            'slug',
            'url',
            'transactions'
        )
        extra_kwargs = {
            'url': {'view_name': 'category-detail', 'lookup_field': 'slug'}
        }

# Put, Patch, Post
class CategoryWriteSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = (
            'category_name',
            'slug',
        )

class TransactionUploadsSerializer(serializers.HyperlinkedModelSerializer):
    file_name = serializers.SerializerMethodField()

    def get_file_name(self, upload):
        return upload.get_file_name()

    class Meta:
        model = TransactionUploads
        fields = [
            'id',
            'file',
            'file_name',
            'uploaded_at',
            'url'
        ]
        read_only_fields = ['id', 'uploaded_at', 'url']
        extra_kwargs = {
            'url': {'view_name': 'transaction-uploads-detail', 'lookup_field': 'id'}
        }

class TransactionDetailsSerializer(serializers.ModelSerializer):
    transactions = NestedTransactionSerializer(many=True, read_only=True)
    summary_url = serializers.SerializerMethodField()

    def get_summary_url(self, transaction_upload):
        # We'll be using reverse() to access our url view name which requires request 
        request = self.context.get('request')
        return reverse('summary-transaction-uploads', args=[transaction_upload.id], request=request, format=None)

    class Meta:
        model = TransactionUploads
        fields = [
            'id',
            'file',
            'uploaded_at',
            'summary_url',
            'transactions',
        ]
        