from rest_framework import serializers
from core.models import UserProfile, Catagory, Post, Comment, Save, ChatMassage
from django.contrib.auth.models import User


class UserS(serializers.ModelSerializer):
    profile = serializers.ImageField(source='user_profile.profileimg')
    is_followed = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profile', 'is_followed','messages_count']
    
    def get_is_followed(self, obj):
        user = self.context['request'].user
        user = UserProfile.objects.get(user=user)
        all = []
        for i in obj.followings.all():
            all.append(i)
        return True if user in all else False
    def get_messages_count(self, obj):
        user = self.context['request'].user
        user = UserProfile.objects.get(user=user)
        u = UserProfile.objects.get(user=User.objects.get(username=obj.username))
        messages = ChatMassage.objects.filter(sender=u, receiver=user, is_show=False)
        return messages.count()


class UserPostS(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.user.username')
    user_profileimg = serializers.ImageField(source = 'user.profileimg')
    catagory = serializers.CharField(source = 'catagory.name')
    #comments = serializers.CharField(source = 'post_comment.all')



    #comments = commentS(source='post_comment.all',many=True)
    comments = serializers.CharField(source = 'post_comment.all')
    comments_count = serializers.CharField(source = 'post_comment.all.count')

    class Meta:
        model = Post
        fields = ['username', 'user_profileimg', 'id' , 'catagory' , 'image' , 'description', 'created_at','likes','dislikes', 'comments','comments_count']
        #fields = '__all__'
        


class userProfileS(serializers.ModelSerializer):
    #user_post = serializers.StringRelatedField(many=True)
    #user_post = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    ##user_post = serializers.HyperlinkedRelatedField( many=True, read_only=True, view_name='track-detail')
    #user_post = serializers.SlugRelatedField( many=True, read_only=True, slug_field='description' )
    ##user_post = serializers.HyperlinkedIdentityField(view_name='description')
    #user_post = PostSForUser(many=True, read_only=True)
    ##user_post = serializers.RelatedField(read_only=True, many=True)
    #a = serializers.CharField(source='user.email')

    #all = serializers.SerializerMethodField(read_only=True)
    #user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    user = UserS()
    friend = UserS(many=True)
    follower = UserS(many=True)
    following = UserS(many=True)
    follower_count = serializers.IntegerField(source="follower.count")
    following_count = serializers.IntegerField(source="following.count")

    user_posts = UserPostS(source='user_post.all', many=True)

    is_followed = serializers.SerializerMethodField()
    messages = serializers.SerializerMethodField()
    messages_count = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = ['id','user','location','bio','follower_count','following_count','profileimg', 'friend','follower','following','user_posts','is_followed','messages','messages_count']
        #read_only_fields = ('location','user', 'follower_count','following_count','profileimg','friend','follower',)
        #read_only_fields = ('location', 'bio', 'follower_count',)
        #extra_kwargs =  {"location": {"read_only": True}}
        
        #fields = '__all__'

    def get_is_followed(self, obj):
        user = self.context['request'].user
        #user = User.objects.get(username=user)
        all = []
        for i in obj.follower.all():
            all.append(i)
        return True if user in all else False
    
    # def get_messages(self, obj):
    #     friends = obj.friend.all()
    #     messages = ChatMassage.objects.filter(sender__user__in=friends, receiver__user=obj.user, is_show=False)
    #     return messages.values()

    def get_messages_count(self, obj):
        friends = obj.friend.all()
        messages = ChatMassage.objects.filter(sender__user__in=friends, receiver__user=obj.user, is_show=False)
        return messages.count()
    def get_messages(self, obj):
        friends = obj.friend.all()
        messages = ChatMassage.objects.filter(sender__user__in=friends, receiver__user=obj.user, is_show=False)
        serialized_messages = [self.serialize_message(message) for message in messages]
        return serialized_messages

    def serialize_message(self, message):
        return {
            'id': message.id,
            'username': message.sender.user.username,
            'profileimg':f"http://127.0.0.1:8000/{message.sender.profileimg.url}",
            'message': message.massage,
            'created_at': message.get_created_at(),
            'find_typecheck': message.find_typecheck()
        }


class catagoryS(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ['id','name']


class commentS(serializers.ModelSerializer):
    senderinfo = serializers.SerializerMethodField(read_only=True)
    is_like = serializers.SerializerMethodField()
    likes_count = serializers.CharField(source = 'likes.all.count', read_only=True)
    class Meta:
        model = Comment
        fields = ['id','post_id','comment', 'senderinfo', 'get_created_at', 'is_like','likes_count']

    def get_senderinfo(self, obj):
        return{
            'username':obj.username.user.username,
            'user_profileimg':f"http://127.0.0.1:8000/{obj.username.profileimg.url}",
        }
    
    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        userp = UserProfile.objects.get(user=user)
        c = Comment(
            username=userp,
            comment=validated_data['comment'],
            post_id=validated_data['post_id']
        )
        c.save()
        return c
    def get_is_like(self, obj):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        if userp in obj.likes.all():
            return True
        else:
            return False
        

class PostS(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.user.username', read_only=True)
    #user = serializers.CharField(source = 'user.user.username')
    #userp = UserProfile.objects.get(user=User.objects.get(username=user)) 
    user_profileimg = serializers.ImageField(source = 'user.profileimg', read_only=True)
    #catagory = serializers.CharField(source = 'catagory.name')
    #comments = serializers.CharField(source = 'post_comment.all')

    comments = commentS(source='post_comment.all',many=True, read_only=True)
    likes_count = serializers.CharField(source = 'likes.all.count', read_only=True)
    dislikes_count = serializers.CharField(source = 'dislikes.all.count', read_only=True)
    comments_count = serializers.CharField(source = 'post_comment.all.count', read_only=True)

    is_save = serializers.SerializerMethodField()
    is_like = serializers.SerializerMethodField()
    is_comment = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['username', 'user_profileimg', 'id' , 'catagory' , 'image' , 'description', 'created_at','likes','dislikes', 'comments','likes_count','dislikes_count','comments_count', 'is_save','is_like','is_comment','find_typecheck','get_created_at']
        #read_only_fields = ('username', 'user_profileimg','id', 'created_at','likes','dislikes', 'comments','likes_count','dislikes_count','comments_count', 'is_save',)
        #fields = '__all__'
        #exclude = ['id']
        
    def get_is_save(self, obj):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        user = UserProfile.objects.get(user=user)
        post_s = []
        for i in obj.post_save.all():
            post_s.append(i.username)
        return True if user in post_s else False
    def get_is_like(self, obj):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        # if userp in obj.likes():
        #     return True
        if obj in userp.post_like.all():
            return True
        else:
            return False
    def get_is_comment(self, obj):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        # if userp in obj.likes():
        #     return True
        all = obj.post_comment.all()
        c=[]
        for i in all:
            c.append(i.username)
        if userp in c:
            return True
        else:
            return False

    def create(self, validated_data):
        user = self.context['request'].user
        user = User.objects.get(username=user)
        userp = UserProfile.objects.get(user=user)
        post = Post(
            user=userp,
            catagory=validated_data['catagory'],
            image=validated_data['image'],
            description=validated_data['description']
        )
        post.save()
        return post
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = User.objects.create(**validated_data)
    #     Post.objects.create(user=user, **profile_data)
    #     return user
    # def create(self, validated_data):
    #     profile_data = validated_data.pop('profile')
    #     user = self.context['request'].user
    #     user = User.objects.get(username=user)
    #     userp = UserProfile.objects.get(user=user)
    #     Post.objects.create(user=userp, **profile_data)
    #     return user
    
    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     post = Post.objects.create(user=user, **validated_data)
    #     return post







class saveS(serializers.ModelSerializer):
    saves = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Save
        fields = ['saves']

    def get_saves(self, obj):
        return {
        "username": obj.username.user.username,
        "user_profileimg": f"http://127.0.0.1:8000/{obj.post_id.user.profileimg.url}",
        "id": obj.id,
        "catagory": obj.post_id.catagory.name,
        "image": f"http://127.0.0.1:8000/{obj.post_id.image.url}",
        "description": obj.post_id.description,
        "created_at": obj.post_id.created_at,
        "likes_count": obj.post_id.likes.count(),
        "dislikes_count": obj.post_id.dislikes.count(),
        "comments_count": obj.post_id.no_of_comments,
        "find_typecheck": obj.post_id.image.url.split('.')[-1]
    }
class chatmassageS(serializers.ModelSerializer):
    sender = serializers.CharField(source = 'sender.user.username')
    receiver = serializers.CharField(source = 'receiver.user.username')
    class Meta:
        model = ChatMassage
        fields = ['id', 'sender', 'receiver', 'massage', 'file', 'find_typecheck', 'is_show', 'get_created_at']



            # ---------------------------------#
            #         for post and put         #
            # ---------------------------------#

#from django.contrib.auth.hashers import make_password
class userRegisterS(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        #extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            #password = make_password(validated_data['password'])
            #password = validated_data['password']
        )
        user.set_password(validated_data['password'])
        user.save()
        userp = UserProfile.objects.create(user = user)
        userp.friend.add(user)
        userp.save()
        return user


class userFollowS(serializers.ModelSerializer):
    u = serializers.CharField(write_only=True)
    class Meta:
        model = UserProfile
        fields = ['u']
    def update(self, instance, validated_data):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        
        userf = User.objects.get(username = validated_data['u'])
        userfp = UserProfile.objects.get(user=userf)


        all = userp.following.all()

        if userf in all:
            userp.following.remove(userf)
            userfp.follower.remove(user)
            print(f'{userp.user.username} -- Unfollowed -- {userfp.user.username}')
        else:
            userp.following.add(userf)
            userfp.follower.add(user)
            print(f'{userp.user.username} -- followed -- {userfp.user.username}')
        return 1


class PostLikeS(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = []
    def update(self, instance, validated_data):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        pk = instance.pk
        post = Post.objects.get(id=pk)

        if userp in post.likes.all():
            post.likes.remove(userp)
            post.save()
            print("unlike")
        else:
            post.likes.add(userp)
            post.save()
            print("like")
        return instance

class saveFormS(serializers.ModelSerializer):
    post = serializers.CharField(write_only=True)
    class Meta:
        model = Save
        fields = ['post','id']

    def create(self, validated_data):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        post = Post.objects.get(id=validated_data['post'])
        if Save.objects.filter(post_id=post,username=userp):
            delsave = Save.objects.get(post_id=post,username=userp)
            delsave.delete()
            print("unsave")
        else:
            newsave = Save(post_id=post,username=userp)
            newsave.save()
            print("save")
        return 'created suc'

    def update(self, instance, validated_data):
        pk = instance.pk
        save = Save.objects.get(id=pk)
        save.delete()
        print("unsaveddd")
        return instance


class CommentLikeS(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = []
    def update(self, instance, validated_data):
        user = self.context['request'].user
        userp = UserProfile.objects.get(user=user)
        pk = instance.pk
        c = Comment.objects.get(id=pk)

        if userp in c.likes.all():
            c.likes.remove(userp)
            c.save()
            print("unlike")
        else:
            c.likes.add(userp)
            c.save()
            print("like")
        return instance



class userProfileFormS(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [ 'profileimg','bio']






        













"""
class PostSForUser(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user' , 'catagory' , 'image' , 'description', 'created_at']
class userS(serializers.ModelSerializer):
    #user_post = serializers.StringRelatedField(many=True)
    #user_post = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    ##user_post = serializers.HyperlinkedRelatedField( many=True, read_only=True, view_name='track-detail')
    #user_post = serializers.SlugRelatedField( many=True, read_only=True, slug_field='description' )
    ##user_post = serializers.HyperlinkedIdentityField(view_name='description')
    user_post = PostSForUser(many=True, read_only=True)
    ##user_post = serializers.RelatedField(read_only=True, many=True)

    all = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ['username','password', 'email', 'profileimg', 'user_post', 'all']

    def get_all(self, obj):
        return{
            'post':obj.user.post_set.all
        }


class catagoryS(serializers.ModelSerializer):
    class Meta:
        model = Catagory
        fields = ['name']

class PostS(serializers.ModelSerializer):
    username = serializers.CharField(source = 'user.username')
    user_profileimg = serializers.ImageField(source = 'user.profileimg')
    catagory = serializers.CharField(source = 'catagory.name')
    class Meta:
        model = Post
        fields = ['username', 'user_profileimg', 'id' , 'catagory' , 'image' , 'description', 'created_at']


class commentS(serializers.ModelSerializer):
    senderinfo = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Comment
        fields = ['post_id', 'username' , 'comment', 'senderinfo']

    def get_senderinfo(self, obj):
        return{
            'username':obj.username.username,
            'user_profileimg':f"http://127.0.0.1:8000/{obj.username.profileimg.url}",
            'post_catagroy':obj.post_id.catagory.name,
            # 'all':obj.username.Post_set.all
        }



class saveS(serializers.ModelSerializer):
    class Meta:
        model = Save
        fields = ['post_id', 'username']


class chatmassageS(serializers.ModelSerializer):
    class Meta:
        model = ChatMassage
        fields = ['sender', 'receiver', 'massage']
"""











