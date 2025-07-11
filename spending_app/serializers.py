from rest_framework import serializers
from .models import Category, Transactions


# GET method
class TransactionReadSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.SerializerMethodField()

    def get_category_name(self, transaction):
        return transaction.category.category_name

    class Meta: 
        model = Transactions
        fields = (
            'id',
            'vendor',
            'amount',
            'date',
            'category_name',
            'category',
            'url'
        )
        extra_kwargs = {
            'category': {'view_name': 'category-detail', 'lookup_field': 'slug'}
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