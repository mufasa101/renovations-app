from django.urls import path
from . import views
app_name = "property"


urlpatterns = [
    path('', views.Index.as_view(), name="index"),
    path('add/', views.Add.as_view(), name="add"),
    path('test/', views.test, name="test"),
    path('import_property/', views.import_property, name="import_property"),
    path('property-rud/<int:id>/', views.EditDelete_property.as_view(), name='property-rud'),
    path('property-listcreate/', views.ListCreate_property.as_view(), name='property-listcreate'),
    path('property-excel/', views.ListCreate_property_excel.as_view(), name='property-excel'),
    # path('dashboard/', views.dashboard.as_view(), name="dashboard"),
    # path('property/', views.property.as_view(), name="property"),
    # path('get_unit_details/<int:id>', views.get_unit_details, name="get_unit_details"),
    # path('units/', views.units.as_view(), name="units"),
    # # path('hello/', views.hello.as_view(), name="hello"),



    # path('construction/', views.construction.as_view(), name="construction"),
   
    # path('unit-detail/<int:unit>/', views.unit_detail.as_view(), name="unit-detail"),
    # path('unit-detail2/<int:unit>/', views.unit_detail2.as_view(), name="unit-detail2"),
    # path('units/<int:property>/', views.units.as_view(), name="units"),
    # path('update_units/', views.unit_update, name="update-units"),
    # path('prepare/', views.prepare_unit, name="prepare-unit"),
    
    
    # path('property/<int:property>/', views.property_detail.as_view(), name="details"),
    # path('property-rud/<int:id>/', views.EditDelete_property.as_view(), name='property-rud'),
    # path('property-listcreate/', views.ListCreate_property.as_view(), name='property-listcreate'),
    # path('documents-listcreate/', views.ListCreate_documents.as_view(), name='documents-listcreate'),
    # path('documents-rud/<int:id>/', views.EditDelete_documents.as_view(), name='documents-rud'),
    # path('utility-listcreate/', views.ListCreate_utility.as_view(), name='utility-listcreate'),
    # path('utility-rud/<int:id>/', views.EditDelete_utility.as_view(), name='utility-rud'),
    
    # path('units-rud/<int:id>/', views.EditDelete_units.as_view(), name='units-rud'),
    # path('units-listcreate/', views.ListCreate_units.as_view(), name='units-listcreate'),
    # path('unit-property-rud/<int:unit_property>/', views.EditDelete_units2.as_view(), name='unit-property-rud'),


    # path('features-listcreate/', views.ListCreate_features.as_view(), name='features-listcreate'),
    # path('features-rud/<int:id>/', views.EditDelete_features.as_view(), name='features-rud'),

    # path('photos-listcreate/', views.ListCreate_photos.as_view(), name='photos-listcreate'),
    # path('photos-rud/<int:id>/', views.EditDelete_photos.as_view(), name='photos-rud'),

]
