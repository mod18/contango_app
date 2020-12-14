from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('welcome/', views.welcome, name='welcome'),
    path('', RedirectView.as_view(url='welcome')),
    path('home/', views.home, name='home'),
    path('home/manage/', views.manage_categories, name='manage-categories'),
    path('ticker/<str:ticker_name>', views.ticker_detail, name='ticker-detail'),
    path('category/<str:category_name>', views.category_detail, name='category-detail'),
    path('category/create/', views.CategoryCreate.as_view(), name='category-create'),
    path('category/<int:pk>/update/', views.CategoryUpdate.as_view(), name='category-update'),
    path('category/<int:pk>/delete', views.CategoryDelete.as_view(), name='category-delete'),
    path('follow_unfollow/', views.follow_unfollow_category, name='follow-unfollow-view'),
]