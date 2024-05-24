from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('user', views.user, basename='user')
router.register('catagory', views.catagory, basename='catagory')
router.register('post', views.post, basename='post')
router.register('posts', views.posts, basename='posts')
router.register('comment', views.comment, basename='comment')
router.register('save', views.save, basename='save')
router.register('userRegister', views.userRegister, basename='userRegister')
router.register('userFollow', views.userFollow, basename='userFollow')
router.register('PostLike', views.PostLike, basename='PostLike')
router.register('saveForm', views.saveForm, basename='saveForm')
router.register('CommentLike', views.CommentLike, basename='CommentLike')
router.register('userProfileForm', views.userProfileForm, basename='userProfileForm')

router.register(r'chatMassage', views.chatMassage, basename='chatMassage')


from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenViewBase, TokenObtainSlidingView, TokenRefreshSlidingView, TokenVerifyView, TokenBlacklistView


urlpatterns = [
    path('', include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="get_token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("api-auth/", include("rest_framework.urls")),
    path('home/', views.home.as_view(), name='home'),
    path('homee/', views.homee, name='homee'),
    path('chatM/<str:pk>', views.chatM.as_view(), name='chatM'),

    # path("a/", TokenViewBase.as_view(), name="a"),
    # path("b/", TokenObtainSlidingView.as_view(), name="b"),
    # path("c/", TokenRefreshSlidingView.as_view(), name="c"),
    # path("d/", TokenVerifyView.as_view(), name="d"),
    # path("e/", TokenBlacklistView.as_view(), name="e"),

]





    






