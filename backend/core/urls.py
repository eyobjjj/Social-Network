from django.urls import path, include
from . import views
 
urlpatterns = [
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.logoutt, name='logout'),
    path('settings/', views.settings, name='settings'),
    path('upload/', views.upload, name='upload'),
    path('like_post/', views.like_post, name='like_post'),
    path('dislike_post/', views.dislike_post, name='dislike_post'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('follow/', views.follow, name='follow'),
    # path('delete_post/<str:pk>', views.delete_post, name='delete_post'),
    # path('edit_post/<str:pk>', views.edit_post, name='edit_post'),
    # path('search/', views.search, name='search'),
    path('postroom/<str:pk>', views.postroom, name='postroom'),
    path('addsave/<str:pk>', views.addsave, name='addsave'),
    path('chat/', views.chat, name='chat'),
    path('singlechat/<str:pk>', views.singlechat, name='singlechat'),
    path('users/', views.users, name='users'),

]






