import rest_framework.fields
from rest_framework.viewsets import ModelViewSet
from core.models import UserProfile, Catagory, Post, Comment, Save, ChatMassage
from .serializer import userProfileS, catagoryS, PostS, commentS, saveS, chatmassageS, userRegisterS, userFollowS, PostLikeS,saveFormS,CommentLikeS,userProfileFormS
from django.contrib.auth.models import User

# from rest_framework.decorators import api_view, authentication_classes, permission_classes
# from rest_framework.authentication import SessionAuthentication, TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework import status

# from django.shortcuts import get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .filter import PostFilter, UserFilter

class home(APIView):
    queryset = Post.objects.all()
    serializer_class = PostS

    def get(self, request, format=None):
        u = User.objects.get(username=request.user)
        up = UserProfile.objects.get(user=u)
        filter_post = Post.objects.filter(user=up)
        serializer_data = self.serializer_class(filter_post, many=True)
        return Response(serializer_data.data)


@api_view(['GET'])
def homee(request):
    u = User.objects.get(username=request.user)
    up = UserProfile.objects.get(user=u)
    p = Post.objects.filter(user=up)
    sd = PostS(p, many=True)
    return Response(sd.data)


from rest_framework.permissions import IsAuthenticated, AllowAny
class userRegister(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = userRegisterS
    lookup_field = 'username'
    permission_classes = [AllowAny]


class user(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = userProfileS
    lookup_field = 'user__username'
    filter_backends = [DjangoFilterBackend]
    filterset_class = UserFilter

    # def list(self, request, *args, **kwargs):
    #     response = super().list(request, *args, **kwargs)
    #     response.data = [response.data]
    #     return response
    
    # def retrieve(self, request, *args, **kwargs):
    #     r = super().retrieve(request, *args, **kwargs)
    #     r.data = [r.data]
    #     return r




class catagory(ModelViewSet):
    queryset = Catagory.objects.all()
    serializer_class = catagoryS

# @authentication_classes([SessionAuthentication, TokenAuthentication])
# @permission_classes([IsAuthenticated])
class post(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostS
    # lookup_field = 'user__username'
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['catagory', 'user']

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply your filters here
        # For example, filter by user
        user = self.request.user
        userp = UserProfile.objects.get(user=user)
        all = userp.following.all()

        queryset = queryset.filter(user__user__in=all)

        return queryset

class posts(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostS
    filter_backends = [DjangoFilterBackend]
    #filterset_fields = ['catagory', 'user', 'description']
    filterset_class = PostFilter
    
class PostLike(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostLikeS

class CommentLike(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentLikeS
    lookup_field = "pk"



class comment(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = commentS


class save(ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = saveS

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        userp = UserProfile.objects.get(user=user)
        queryset = queryset.filter(username=userp)
        return queryset

class saveForm(ModelViewSet):
    queryset = Save.objects.all()
    serializer_class = saveFormS

# class chatMassage(ModelViewSet):
#     serializer_class = chatmassageS
#     #lookup_field = 'receiver'

#     def get_queryset(self):
#         queryset = ChatMassage.objects.all()
#         user = self.request.user
#         #pk = self.kwargs.get('receiver')
#         pk = self.kwargs.get('pk')

#         if pk is not None:
#             # user = User.objects.get(username = user)
#             # userp = UserProfile.objects.get(user = user)
#             # friend = User.objects.get(id = pk)
#             # friendp = UserProfile.objects.get(user = friend)
#             # #friend = UserProfile.objects.get(user__username=receiver)

#             # messages = ChatMassage.objects.filter(sender=userp , receiver=friendp)# | ChatMassage.objects.filter(sender=friendp , receiver=userp)

#             # p=ChatMassage.objects.get(id=1)
#             # print(p.massage)
#             queryset = ChatMassage.objects.all()
#         return queryset



from rest_framework.decorators import action
class chatMassage(ModelViewSet):
    queryset = ChatMassage.objects.all()
    serializer_class = chatmassageS

    @action(detail=True, methods=['get', 'post'])
    def singlechat(self, request, pk=None):
        user = request.user
        userp = UserProfile.objects.get(user=user)
        friend = User.objects.get(username=pk)
        friendp = UserProfile.objects.get(user=friend)

        messages = ChatMassage.objects.filter(sender=userp, receiver=friendp) | ChatMassage.objects.filter(sender=friendp, receiver=userp)
        serializer = self.get_serializer(messages, many=True)

        # if pk is not None:
        #     print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        #     return Response(serializer.data)

        if request.method == 'POST':
            new_message = ChatMassage.objects.create(sender=userp, receiver=friendp, massage=request.POST['massage'], file=request.FILES.get('file'))
            new_message.save()

            friend_filter = UserProfile.objects.filter(user=user, friend=friend)
            if friend_filter:
                print(11111111111111111111111111111111111111111111111111111111111111111)
            else:
                new_friend1 = userp.friend.add(friend)
                new_friend2 = friendp.friend.add(user)
                new_friend1.save()
                new_friend2.save()

        return Response(serializer.data)
    
    @action(detail=True, methods=['put'])
    def chatView(self, request, pk=None):
        user = request.user
        userp = UserProfile.objects.get(user=user)
        friend = User.objects.get(username=pk)
        friendp = UserProfile.objects.get(user=friend)

        messages = ChatMassage.objects.filter(sender=friendp, receiver=userp)
        serializer = self.get_serializer(messages, many=True)

        if request.method == 'PUT':

            for i in messages:
                i.is_show = True
                i.save()
                print(i.is_show)

        return Response(serializer.data)



"""
class ChatMassageViewSet(viewsets.ModelViewSet):
    queryset = ChatMassage.objects.all()
    serializer_class = ChatMassageSerializer

    @action(detail=True, methods=['post'])
    def send_message(self, request, pk=None):
        user = self.request.user
        userp = UserProfile.objects.get(user=user)
        friend = User.objects.get(username=pk)
        friendp = UserProfile.objects.get(user=friend)

        message = ChatMassage.objects.filter(sender=userp, receiver=friendp) | ChatMassage.objects.filter(
            sender=friendp, receiver=userp)

        friend_filter = UserProfile.objects.filter(user=user, friend=friend)
        form = ChatMassageForm()
        if request.method == 'POST':
            if friend_filter:
                pass
            else:
                new_friend = userp.friend.add(friend)

            form = ChatMassageForm(request.POST)
            if form.is_valid():
                newMessage = form.save(commit=False)
                newMessage.sender = userp
                newMessage.receiver = friendp
                newMessage.save()

        serializer = self.get_serializer(message, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
"""

class chatM(APIView):
    queryset = ChatMassage.objects.all()
    serializer_class = chatmassageS

    def get(self, request, pk=None, format=None):
        u = User.objects.get(username=request.user)
        up = UserProfile.objects.get(user=u)
        filter_post = ChatMassage.objects.filter()
        serializer_data = self.serializer_class(filter_post, many=True)

        if pk is None:
            return Response(serializer_data.data)
        return Response(serializer_data.data)
    

    
class userFollow(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = userFollowS
    lookup_field = 'user__username'
    #permission_classes = [AllowAny]


class userProfileForm(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = userProfileFormS
    lookup_field = 'user__username'