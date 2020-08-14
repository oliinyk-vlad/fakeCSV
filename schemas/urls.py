from django.urls import path, include
from schemas import views

app_name = 'schemas'

urlpatterns = [
    path('', views.SchemaListView.as_view(), name='list'),
    path('create/', views.SchemaCreateView.as_view(), name='create'),
    path('<int:pk>/', views.SchemaDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', views.SchemaUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', views.SchemaDeleteView.as_view(), name='delete'),
]
