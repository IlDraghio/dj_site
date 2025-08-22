from django.urls import path
from . import views
    
urlpatterns = [
    path('ml/',views.ml_view, name= 'ml'),
    path('preprocessed_data/',views.preprocessed_data_view, name= 'preprocessed_data'),
    path('table_preprocessed_data/',views.preprocessed_view, name= 'table_preprocessed_data'),
    path('export_csv_view/',views.export_csv_view, name= 'export_csv_view'),
]