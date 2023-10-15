from django.contrib import admin
from app.models import *

# Register your models here.
class MediaBuyingAdmin(admin.ModelAdmin):
    list_display = ['id','media_campaign_date','media_name','media_platform','media_product','media_amount','media_date_created']
    search_fields = ['media_product', 'media_name', 'media_platform']
    list_per_page = 8




class MediaBuyingRequestsAdmin(admin.ModelAdmin):
    list_display = ['id', 'media_date_request','media_request', 'media_approx_requests','media_cost_per_request','media_total_impressions','media_total_clicks','media_request_date_created']
    search_fields = ['media_date_request','media_request']
    list_per_page = 8


admin.site.register(Product)
admin.site.register(Platform)
admin.site.register(Reference)
admin.site.register(MediaBuying, MediaBuyingAdmin)
admin.site.register(MediaBuyingRequests, MediaBuyingRequestsAdmin)
