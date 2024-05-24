import django_filters
from core.models import Post, UserProfile



class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = {'description':['icontains']}

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = UserProfile
        fields = {'user__username':['icontains']}




