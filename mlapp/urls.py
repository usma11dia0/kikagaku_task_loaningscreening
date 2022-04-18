from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('input_form/', views.input_form, name='mlapp/input_form'),
    path('result/', views.result, name='result') # 追加
]