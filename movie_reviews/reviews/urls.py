from django.urls import path

from . import views

urlpatterns = [
    path('', views.Reviews.as_view(), name='index'),
    path('load_more/<int:offset>', views.LoadJSONReview.as_view(), name='load_more')
]

