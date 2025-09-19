from django.urls import path
from . import views
urlpatterns = [
    path('category/', views.CategoryView.as_view()),
    path('category/<str:id>/', views.CategoryDetailView.as_view()),
    path('product/', views.ProductView.as_view()),
    path('product/<str:id>/', views.ProductDetailView.as_view()),
    path('addtocart/<str:id>/', views.AddToCartView.as_view()),
]