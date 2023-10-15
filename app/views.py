from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import *
from django.db.models import Sum
from django.db.models import Q
import datetime


# Create your views here.
def index(request):
    products = Product.objects.all()
    platforms = Platform.objects.all()
    references = Reference.objects.all()
    campaigns = MediaBuying.objects.all().order_by('-media_campaign_date')
    context = {
        'campaigns':campaigns,
        'products':products,
        'platforms':platforms,
        'references':references,
    }
    return render(request, 'index.html', context)

    

def mediaAdd(request):
    if request.method == "POST":
        media = MediaBuying()
        media.media_campaign_date = request.POST.get('date')
        media.media_name = request.POST.get('reference')
        media.media_platform = request.POST.get('platform')
        media.media_product = request.POST.get('product')
        media.media_amount = request.POST.get('amount')
        media.media_amount_dollar = request.POST.get('amount_dollar')
        media.save()
        messages.success(request, 'تمت إضافة حملة جديدة بنجاح')
        return redirect('index')
    else:
        return render(request, 'index.html')



def mediaUpdate(request, id):
    update_campaign = MediaBuying.objects.get(id=id)
    if request.method == "POST":
        update_campaign.media_campaign_date = request.POST.get('date')
        update_campaign.media_name = request.POST.get('reference')
        update_campaign.media_platform = request.POST.get('platform')
        update_campaign.media_product = request.POST.get('product')
        update_campaign.media_amount = request.POST.get('amount')
        update_campaign.media_amount_dollar = request.POST.get('amount_dollar')
        update_campaign.save()
        messages.success(request, 'تمت  عملية تحديث الحملة بنجاح')
        return redirect('index')
    else:
        return render(request, 'index.html')



def mediaDelete(request, id):
    delete_campaign = MediaBuying.objects.get(id=id)
    delete_campaign.delete()
    messages.success(request, 'تمت عملية حذف الحملة بنجاح')
    return redirect('index')



def mediaAddRequest(request):
    if request.method == "POST":
        add_request = MediaBuyingRequests()
        add_request.media_request = MediaBuying.objects.get(id=request.POST.get('media_request_id'))
        add_request.media_date_request = request.POST.get('media_date_request')
        add_request.media_approx_requests = request.POST.get('media_approx_requests')
        add_request.media_cost_per_request = request.POST.get('media_cost_per_request')
        add_request.media_total_impressions = request.POST.get('media_total_impressions')
        add_request.media_total_clicks = request.POST.get('media_total_clicks')
        add_request.save()
        messages.success(request, 'تمت إضافة طلبات جديدة')
        return redirect('index')
    else:
        return render(request, 'index.html')



def mediaDetailRequest(request, id):
    selected_campaign = MediaBuying.objects.get(id=id)
    selected_requests = MediaBuyingRequests.objects.filter(media_request=selected_campaign)
    # media_approx_requests = selected_requests.values_list('media_approx_requests', flat=True).count() 
    media_approx_requests = selected_requests.values_list('media_approx_requests', flat=True).aggregate(Sum('media_approx_requests'))['media_approx_requests__sum']
    if media_approx_requests:
        media_cost_per_request = str(round(media_approx_requests / selected_campaign.media_amount,2))
    else:
        media_cost_per_request = 0
    media_total_impressions = selected_requests.values_list('media_total_impressions', flat=True).aggregate(Sum('media_total_impressions'))['media_total_impressions__sum']
    media_total_clicks = selected_requests.values_list('media_total_clicks', flat=True).aggregate(Sum('media_total_clicks'))['media_total_clicks__sum']

    context = {
        'selected_requests':selected_requests,
        'selected_campaign':selected_campaign,
        'media_approx_requests':media_approx_requests,
        'media_cost_per_request':media_cost_per_request,
        'media_total_impressions':media_total_impressions,
        'media_total_clicks':media_total_clicks,
    }
    return render(request, 'detail_request.html', context)




def mediaUpdateRequest(request, id):
    update_request = MediaBuyingRequests.objects.get(id=id)
    campagin_id = update_request.media_request.id
    if request.method == "POST":
        update_request.media_date_request = request.POST.get('media_date_request')
        update_request.media_approx_requests = request.POST.get('media_approx_requests')
        update_request.media_cost_per_request = request.POST.get('media_cost_per_request')
        update_request.media_total_impressions = request.POST.get('media_total_impressions')
        update_request.media_total_clicks = request.POST.get('media_total_clicks')
        update_request.save()
        messages.success(request, 'تمت  عملية تحديث الطلبات بنجاح')
        return redirect('detail_request', campagin_id)
        # return render(request, 'detail_request.html')
    else:
        return render(request, 'detail_request.html')

    


def mediaDeleteRequest(request, id):
    delete_request = MediaBuyingRequests.objects.get(id=id)
    delete_request.delete()
    messages.success(request, 'تمت عملية حذف الطلبات بنجاح')
    return render(request, 'detail_request.html')





def isValid(params):
    return params != '' and params is not None



def MediaBuyingReport(request):

    pf = [e.platform_name for e in Platform.objects.all()]

    querySets = MediaBuying.objects.all()


    platforms = MediaBuying.objects.order_by('media_platform').values_list('media_platform', flat=True).distinct()
    references = MediaBuying.objects.order_by('media_name').values_list('media_name', flat=True).distinct()
    products = MediaBuying.objects.order_by('media_product').values_list('media_product', flat=True).distinct()

    q_date_from = request.GET.get('date_from')
    q_date_to = request.GET.get('date_to')
    q_platform = request.GET.get('report_platform')
    q_reference = request.GET.get('report_reference')
    q_product = request.GET.get('report_product')


    
    if isValid(q_date_from) & isValid(q_date_to):
        querySets = querySets.filter(mediabuyingrequests__media_date_request__gte=q_date_from, mediabuyingrequests__media_date_request__lte=q_date_to)


    if isValid(q_platform):
        querySets = querySets.filter(media_platform__exact=q_platform)


    if isValid(q_reference):
        querySets = querySets.filter(media_name__exact=q_reference)


    if isValid(q_product):
        querySets = querySets.filter(media_product__exact=q_product)
    

    




    total_amount = querySets.values_list('media_amount', flat=True).distinct().aggregate(Sum('media_amount'))['media_amount__sum']
    total_requests = querySets.values_list('mediabuyingrequests__media_approx_requests', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_approx_requests'))['mediabuyingrequests__media_approx_requests__sum']
    
    if total_requests:
        total_cost_per_request = str(round(total_requests/total_amount,3))
    else:
        total_cost_per_request = ''

    total_impressions = querySets.values_list('mediabuyingrequests__media_total_impressions', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_total_impressions'))['mediabuyingrequests__media_total_impressions__sum']
    total_clicks = querySets.values_list('mediabuyingrequests__media_total_clicks', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_total_clicks'))['mediabuyingrequests__media_total_clicks__sum']

    labels = []
    data_request = []
    data_impression = []
    data_click = []
    for x in pf:
        labels.append(x)
        temp = querySets.filter(media_platform=x).values_list('mediabuyingrequests__media_approx_requests', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_approx_requests'))['mediabuyingrequests__media_approx_requests__sum']
        if temp == None:
            data_request.append(0)
        else:
            data_request.append(temp)
    

    for x in pf:
        temp = querySets.filter(media_platform=x).values_list('mediabuyingrequests__media_total_impressions', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_total_impressions'))['mediabuyingrequests__media_total_impressions__sum']
        if temp == None:
            data_impression.append(0)
        else:
            data_impression.append(temp)



    for x in pf:
        temp = querySets.filter(media_platform=x).values_list('mediabuyingrequests__media_total_clicks', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_total_clicks'))['mediabuyingrequests__media_total_clicks__sum']
        if temp == None:
            data_click.append(0)
        else:
            data_click.append(temp)
        

    weekday = [1, 2, 3, 4, 5, 6, 7]
    data_weekday = []
    for x in weekday:
        temp = querySets.filter(mediabuyingrequests__media_date_request__week_day=x).values_list('mediabuyingrequests__media_approx_requests', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_approx_requests'))['mediabuyingrequests__media_approx_requests__sum']   
        if temp == None:
            data_weekday.append(0)
        else:
            data_weekday.append(temp)



    
    month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    data_month = []
    for x in month:
        temp = querySets.filter(mediabuyingrequests__media_date_request__month=x).values_list('mediabuyingrequests__media_approx_requests', flat=True).distinct().aggregate(Sum('mediabuyingrequests__media_approx_requests'))['mediabuyingrequests__media_approx_requests__sum']   
        if temp == None:
            data_month.append(0)
        else:
            data_month.append(temp)


    context = {
        'platforms':platforms,
        'references':references,
        'products':products,
        'total_amount':total_amount,
        'total_requests':total_requests,
        'total_cost_per_request':total_cost_per_request,
        'total_impressions':total_impressions,
        'total_clicks':total_clicks,
        'labels':labels,
        'data_request':data_request,
        'data_impression':data_impression,
        'data_click':data_click,
        'data_weekday':data_weekday,
        'data_month':data_month,
        'q_date_from':q_date_from,
    }
    return render(request, 'mediabuying_report.html', context)

    






