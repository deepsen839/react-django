from django.urls import path
from crud import views
urlpatterns = [
    path('', views.get_all_items),
    path('get-user-events/<int:id>/', views.get_user_events,name="get-user-events"),
    path('get-single-item/<int:id>/', views.get_single_items,name="get-single-item"),
    path('post-item/', views.post_items,name="post-item"),
    path('update-item/<int:id>/', views.update_item,name="update-item"),
    path('register/', views.regiserUser, name='register'),
    path('event-liked/', views.update_event_like, name='event-liked'),

]