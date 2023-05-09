from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import EventsModel,EventsLiked
from django.contrib.auth.models import User

from .serializers import EventSerializer,RegisterSerializer,EventsLikedSerializer
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from django.db.models import Prefetch
# Create your views here.
@api_view(['POST','GET'])
@permission_classes([AllowAny])
def get_all_items(request):
    events = EventsModel.objects.prefetch_related(Prefetch('user_details',queryset=EventsLiked.objects.all())).all()
    serializer = EventSerializer(events,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_user_events(request,id):
    events = EventsModel.objects.prefetch_related(Prefetch('user_details',queryset=EventsLiked.objects.all())).filter(created_by=id).all()
    serializer = EventSerializer(events,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)


@api_view(['GET'])
def get_single_items(request,id):
    events = EventsModel.objects.filter(pk=id).prefetch_related(Prefetch('user_details',queryset=EventsLiked.objects.all())).first()
    serializer = EventSerializer(events)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['POST','GET'])
def post_items(request):
    if request.method=='POST':
        event_serializer = EventSerializer(data=request.data)
        if event_serializer.is_valid():
            event_serializer.save()
            return Response(event_serializer.data, status=status.HTTP_201_CREATED)
        else:
            print('error', event_serializer.errors)
            return Response(event_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'mesage':"please post item"})

@api_view(['PUT','PATCH'])
def update_item(request,id):
    events_data = EventsModel.objects.filter(pk=id).first()
    serializer = EventSerializer(events_data, data=request.data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST','GET'])
@permission_classes([AllowAny])
def regiserUser(request):
    if request.method == 'POST':
        user_serializer = RegisterSerializer(data=request.data)
        if user_serializer.is_valid():
            account = user_serializer.save()
            account.is_active = True
            account.save()
            data = {"message":"user registration successgul"}
        else:
            data = user_serializer.errors
        return Response(data)
    return Response({"message":"please enter register"})
@api_view(['POST'])
def update_event_like(request):
    events_data = EventsModel.objects.filter(pk=request.POST.get('event_id')).first()
    is_liked = int(events_data.is_liked) + 1 
    event_serializer = EventSerializer(events_data, data={'is_liked':is_liked},partial=True)

    event_liked_serializer = EventsLikedSerializer(data = {'likedby':request.POST.get('user_id'),'events':request.POST.get('event_id')})
    if event_liked_serializer.is_valid() and event_serializer.is_valid():
        event_liked_serializer.save()
        event_serializer.save()
        return Response({"message": "success", "data": event_liked_serializer.data}, status=status.HTTP_200_OK)
    return Response({"message": "success", "data": event_liked_serializer.errors})
