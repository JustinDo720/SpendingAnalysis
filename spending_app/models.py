from django.db import models
from django.utils.text import slugify
import os

# Create your models here.

class Category(models.Model):
    """
        Each Transaction should be tied to a specific category

        category_name: The name of our category 
        slug: Identifier for the category 
    """
    category_name = models.CharField(max_length=125, unique=True)
    slug = models.SlugField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.category_name)
            gen_slug = base_slug
            cnt = 1

            while Category.objects.filter(slug=gen_slug).exists():
                gen_slug = f'{base_slug}-{cnt}'
                cnt += 1
            
            self.slug = gen_slug
        
        # Regardless we need to super save 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.category_name


class TransactionUploads(models.Model):
    file = models.FileField(upload_to='transaction_uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def get_file_name(self):
        return os.path.basename(self.file.name)


class Transactions(models.Model):
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
    transaction_upload = models.ForeignKey(TransactionUploads, on_delete=models.CASCADE, related_name='transactions')

    def __str__(self):
        return f'{self.vendor}[{self.category.category_name}]: ${self.amount}'    
