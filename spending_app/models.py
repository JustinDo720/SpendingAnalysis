from django.db import models

# Create your models here.

class Category(models.Model):
    """
        Each Transaction should be tied to a specific category

        category_name: The name of our category 
    """
    category_name = models.CharField(max_length=125, unique=True)

    def __str__(self):
        return self.category_name

class Transations(models.Model):
    """
        Each Transaction instance is within the CSV 

        date: Date of the transaction
        vendor: Name of who was paid 
        amount: How much we paid the vendor 
        category: Grouping the payment  
    """
    vendor = models.CharField(max_length=155)
    amount = models.DecimalField(max_digits=19, decimal_places=2)
    date = models.DateField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.vendor}[{self.category.category_name}]: ${self.amount}'
    
    
