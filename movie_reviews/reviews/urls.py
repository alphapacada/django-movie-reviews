from django.urls import path
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.Reviews.as_view(), name='index'),
    path('load_more/<int:offset>', views.LoadMoreReviews.as_view(), name='load_more'),
    path('bookmark/', views.add_bookmark, name='add_bookmark'),
    path('bookmarks/', login_required(views.Bookmarks.as_view()), name='bookmarks'),
    path('add-folder/<pk>', views.FolderCreateView.as_view(), name='add-folder'),
    path('add-to-folders/<pk>/', views.AddToFoldersView.as_view(), name='add-to-folders'),
    path('search/', views.Reviews.as_view(), {'title': 'Search'}, name='search'),
    path('accounts/signup/', views.SignUpView.as_view(), name='signup'),
]   

