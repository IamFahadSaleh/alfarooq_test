from django.db import models

# Create your models here.
class Product(models.Model):
    product_name = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.product_name
    


class Platform(models.Model):
    platform_name = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.platform_name



class Reference(models.Model):
    reference_name = models.CharField(max_length=300,null=True)

    def __str__(self):
        return self.reference_name



class MediaBuying(models.Model):
    media_campaign_date = models.DateField()
    media_name = models.CharField(max_length=300,null=True)
    media_platform = models.CharField(max_length=300,null=True)
    media_product = models.CharField(max_length=300,null=True)
    media_amount = models.DecimalField(max_digits=8, null=True, decimal_places = 2)
    media_amount_dollar = models.DecimalField(max_digits=8, null=True, decimal_places = 2)
    media_date_created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return f'{self.id}'



class MediaBuyingRequests(models.Model):
    media_request = models.ForeignKey(MediaBuying, null=True, on_delete=models.CASCADE)
    media_date_request = models.DateField(null=True)
    media_approx_requests = models.IntegerField(null=True)
    media_cost_per_request = models.DecimalField(max_digits=8, null=True, decimal_places = 2)
    media_total_impressions = models.IntegerField(null=True)
    media_total_clicks = models.IntegerField(null=True)
    media_request_date_created = models.DateTimeField(auto_now_add=True,null=True)


