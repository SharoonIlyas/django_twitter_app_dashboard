from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.models import User
from .models import Tweet

from django.http import JsonResponse

from django.contrib.auth.models import User
from .models import Tweet 
from .serializers import TweetSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework import status

from django.db.models import Q



@api_view(['Get',])
@permission_classes([IsAuthenticated])
def api_tweet_view(request):
    tweet = Tweet.objects.all()
    serializer = TweetSerializer(tweet, many = True)
    return Response(serializer.data)


@api_view(['Get',])
@permission_classes([IsAuthenticated])
def api_tweet_detail_view(request,pk):
    tweet = Tweet.objects.get(id=pk)
    serializer = TweetSerializer(tweet)
    return Response(serializer.data)


@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_tweet_create_view(request):
    current_user = request.user
    setuser = Tweet(user = current_user)
    serializer = TweetSerializer(setuser, data = request.data)
    if serializer.is_valid():
        serializer.save()
    else:
        return Response('data was not valid')
    return Response(serializer.data)



@api_view(['POST',])
@permission_classes([IsAuthenticated])
def api_tweet_update_view(request,pk):
    tweet = Tweet.objects.get(id=pk)
    serializer = TweetSerializer(instance = tweet , data = request.data)
    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE',])
@permission_classes([IsAuthenticated])
def api_tweet_delete_view(request, pk):
    try:
        tweet = Tweet.objects.get(id=pk)    
        tweet.delete()
        return Response({'data':"Tweet deleted"})
    except:
        return Response({'data':"Tweet does not exist"}, status = 404)

    
##########################################################
@api_view(['POST'])
def user_follow_view(request, username ,*args, **kwargs):
    me = request.user
    other_user_qs = User.objects.filter(username = username)
    
    if me.username == username:
       my_followers = me.profile.followers.all()  
       return Response({"countme":my_followers.count()}, status = 200)
        
    
    if not other_user_qs.exists():
        return Response({}, status = 404)
    other = other_user_qs.first()
    profile = other.profile
    
    data = request.data or {}
    action = data.get("action")
    
        
    if action=="follow":
        profile.followers.add(me)
        
    elif action =="unfollow":
        profile.followers.remove(me)
    else:
        pass  
    
    current_followers_qs = profile.followers.all()  
   # return Response({"count":current_followers_qs.count()})
    print(list(current_followers_qs)) 
  
    return Response({"counting":current_followers_qs.count()})
  
########################################################



''' @login_required
def dasshboard(request):
    current_user = request.user
    profiles = current_user.following.all()
    profiles_exist = current_user.following.exists()
    followed_user_id =[]
    if profiles.exists():
        followed_user_id = current_user.following.values_list("user__id", flat = True)
    qs = Tweet.objects.filter(
        Q(user__id__in =followed_user_id) |
        Q(user = current_user)).distint().order_by("-datetime")
    
    context = {'tweets':qs,'current_user':current_user}
    return render(request, 'tweet/pages/dashboard.html',context) '''



@login_required
def dashboard(request):
    current_user = request.user
    profiles = current_user.following.all()
    followed_user_id =[]
    if profiles.exists():
        followed_user_id = [x.user.id for x in profiles ]
    
    followed_user_id.append(current_user.id)
    
    qs = Tweet.objects.filter(user__id__in =followed_user_id).order_by('-datetime')
    
    tweets = Tweet.objects.all().order_by('-datetime')
    
    print(profiles.count())
    context = {'tweets':qs,'current_user':current_user , 'followed_no':profiles.count()}
    return render(request, 'tweet/pages/dashboard.html',context)






@login_required
def mytweets(request):
    current_user = request.user
    tweets = current_user.tweet_set.all().order_by('-datetime')
    
    context = {'tweets':tweets}
    return render(request, 'tweet/pages/mytweet.html',context)
###
def redirect_view(request):
    response = redirect('dashboard/')
    return response



########################################################################

def findpeople(request):
    users = User.objects.filter(~Q(id = request.user.id))
    current_user = request.user 
    context = {'users':users,'find_followed':current_user.following.all()}
    return render(request, 'tweet/pages/findpeople.html', context)


def followed_page(request):
    current_user = request.user 
    context = {'followed':current_user.following.all()}
        
    return render (request, 'tweet/pages/followed.html', context)


