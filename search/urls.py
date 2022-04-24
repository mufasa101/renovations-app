from django.urls import path
from . import views
app_name = "search"


urlpatterns = [
   path('units/', views.units, name='units'),
   path('contractor/', views.contractor, name='contractor'),

]
