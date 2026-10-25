from django.db import models

# Create your models here.
class invoice(models.Model):
    customer_name=models.CharField(max_length=200)
    invoice_number=models.CharField(max_length=50)
    amount=models.DecimalField( max_digits=12, decimal_places=2)
    date_created=models.DateField(auto_now_add=True)
    is_paid=models.BooleanField(default=False)

    class Meta:
        ordering=['-date_created']
        
    def __str__(self):
        return self.invoice_number