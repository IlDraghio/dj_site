from django.urls import path
from . import views
    
urlpatterns = [
    path('dataset/',views.dataset_view, name= 'dataset'),
    path('new_data/',views.newdata_view, name= 'new_data'),
    path('mass_data/', views.massdata_view, name='mass_data'),
    path('delete_data/', views.delete_data_view, name='delete_data'),
    path('update_data/', views.update_data_view, name='update_data'),    
]