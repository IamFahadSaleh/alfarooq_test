from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('add', views.mediaAdd, name="add"),
    path('update/<str:id>', views.mediaUpdate, name="update"),
    path('delete/<str:id>', views.mediaDelete, name="delete"),
    path('add_request', views.mediaAddRequest, name="add_request"),
    path('detail_request/<str:id>', views.mediaDetailRequest, name="detail_request"),
    path('update_request/<str:id>', views.mediaUpdateRequest, name="update_request"),
    path('delete_request/<str:id>', views.mediaDeleteRequest, name="delete_request"),
    path('mediabuying-report', views.MediaBuyingReport, name="mediabuying_report"),
]
