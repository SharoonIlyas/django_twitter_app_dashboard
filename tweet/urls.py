from django.urls import path , include
from . import views
from .views import user_follow_view


urlpatterns = [
    path('dashboard/', views.dashboard , name = 'dashboard'),
    path('mytweet/', views.mytweets , name = 'mytweet'),
    path('', views.redirect_view),
    path('followed/', views.followed_page , name ='followed'),

    path('api/tweet-list/' , views.api_tweet_view, name = 'api_tweet_view'),    
    path('api/tweet-detail/<str:pk>/' , views.api_tweet_detail_view, name = 'api_tweet_detail_view'),
    path('api/tweet-create/' , views.api_tweet_create_view, name = 'api_tweet_create_view'),

    path('api/tweet-update/<str:pk>/' , views.api_tweet_update_view, name = 'api_tweet_update_view'), 
    path(r'api/tweet-delete/<str:pk>/' , views.api_tweet_delete_view, name = 'api_tweet_delete_view'),


    path('findpeople/',views.findpeople , name ='findpeople'),


    
    path("api/profile/<str:username>/follow/", user_follow_view, name="user_follow_view")
    
]