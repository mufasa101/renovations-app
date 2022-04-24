from django.urls import path
from . import views
app_name = "services"


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('<int:maintenance>/', views.details.as_view(), name="details"),

    path("maintenance-rud/<int:id>/", views.EditDelete_request.as_view(),name="maintenance-rud"),
    path("maintenance-rud/", views.EditDelete_request.as_view(),name="maintenance-rud"),
    path('maintenance-listcreate/', views.ListCreate_request.as_view(), name='maintenance-listcreate'),

    path("cost-rud/<int:id>/", views.EditDelete_cost.as_view(),name="cost-rud"),
    path("cost-rud/", views.EditDelete_cost.as_view(),name="cost-rud"),
    path('cost-listcreate/', views.ListCreate_cost.as_view(), name='cost-listcreate'),
    
    path("services-rud/<int:id>/", views.EditDelete_service.as_view(),name="services-rud"),
    path("services-rud/", views.EditDelete_service.as_view(),name="services-rud"),
    path('services-listcreate/', views.ListCreate_service.as_view(), name='services-listcreate'),

    path("document-rud/<int:id>/", views.EditDelete_document.as_view(),name="document-rud"),
    path("document-rud/", views.EditDelete_document.as_view(),name="document-rud"),
    path('document-listcreate/', views.ListCreate_document.as_view(), name='document-listcreate'),


]
