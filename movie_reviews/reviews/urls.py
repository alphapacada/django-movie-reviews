from django.urls import path

from . import views

urlpatterns = [
    path('', views.Reviews.as_view(), name='index'),
    path('load_more/<int:offset>', views.LoadMoreReviews.as_view(), name='load_more'),
    path('bookmark/', views.add_bookmark, name='add_bookmark'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]

