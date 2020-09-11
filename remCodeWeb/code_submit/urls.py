from django.urls import path

from . import views

urlpatterns = [
    path('', views.get_name, name='index'),
    path('token/<token>/', views.get_code_result, name='get_results'),
]
