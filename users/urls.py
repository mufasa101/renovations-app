from django.urls import path
from . import views
app_name = "users"


urlpatterns = [
       path('', views.admin.as_view(), name="index"),
       path('admin/', views.admin.as_view(), name='admin'),
       path("profile/", views.profile.as_view(),name="profile"),
       path('employee/', views.employee.as_view(), name='employee2'),

       path("Edit_my_profile/<int:id>/", views.Edit_my_profile.as_view(),name="Edit_my_profile"),

       path("admin-rud/<int:id>/", views.EditDelete_admin_profile.as_view(),name="admin-rud"),
       path('admin-listcreate/', views.ListCreate_admin_profile.as_view(), name='admin-listcreate'),

       path("employee-rud/<int:id>/", views.EditDelete_employee_profile.as_view(),name="employee-rud"),
       path('employee-listcreate/', views.ListCreate_employee_profile.as_view(), name='employee-listcreate'),
]
