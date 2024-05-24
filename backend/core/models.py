from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

class Catagory(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User,related_name='user_profile', on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='default-profile-img.jpg')
    location = models.CharField(max_length = 100, blank = True)
    date_joined = models.DateTimeField(auto_now_add=True)
    friend = models.ManyToManyField(User, related_name='friends')
    follower = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='followings', blank=True)
    catagory = models.ManyToManyField(Catagory, related_name='user_catagory', blank=True)

    def __str__(self):
        return f"profile-{self.user.username}"


from django.utils import timezone
from django.utils.timesince import timesince
class Post(models.Model):
    user = models.ForeignKey(UserProfile, related_name='user_post', on_delete=models.CASCADE)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE)
    image = models.FileField(upload_to='post_images',null=True, validators=[FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv', 'apng','avif','gif','jpg','jpeg','jfif','pjpeg','pjp','png','svg','webp','bmp','ico','cur','tif','tiff'])])
    description = models.TextField()
    no_of_comments = models.IntegerField(default=0)
    likes = models.ManyToManyField(UserProfile, related_name='post_like', blank=True)
    dislikes = models.ManyToManyField(UserProfile, related_name='post_dislike', blank=True)
    view = models.ManyToManyField(UserProfile, related_name='post_view', blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = [ '-created_at']

    def __str__(self):
        return self.user.user.username
    
    def find_typecheck(self):
        filename = self.image.name
        ext = filename.split('.')[-1]
        return ext
    # def get_created_at(self):
    #     date = timezone.now() - self.created_at

    #     days = date.days
    #     hours = date.seconds // 3600
    #     minutes = (date.seconds % 3600) // 60
    #     seconds = date.seconds % 60
    #     return f"{days}-{hours}-{minutes}"
    def get_created_at(self):
        date = timesince(self.created_at)
        return date








class Comment(models.Model):
    post_id = models.ForeignKey(Post, related_name='post_comment', on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    comment = models.TextField()
    likes = models.ManyToManyField(UserProfile, related_name='comment_like', blank=True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    class Meta:
        ordering = [ '-updated_at', '-created_at']

    def __str__(self):
        return self.username.user.username
    
    def get_created_at(self):
        date = timesince(self.created_at)
        return date



class Save(models.Model):
    post_id = models.ForeignKey(Post, related_name='post_save', on_delete=models.CASCADE)
    username = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.username.user.username

class ChatMassage(models.Model):
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    massage = models.TextField(blank=True)
    file = models.FileField(upload_to="chat_file", blank=True)
    is_show = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.sender.user.username
    
    class Meta:
        ordering = [ 'timestamp']
    
    def get_created_at(self):
        date = timesince(self.timestamp)[:5]
        return date

    # def __unicode__(self):
    #     return self.file
    
    def find_typecheck(self):
        filename = self.file.name
        ext = filename.split('.')[-1]
        return ext






# class Meta:
#     ordering = ["horn_length"]
#     verbose_name_plural = "oxen"
#     abstract = True
#     proxy = True

# from django.core.mail import send_mail
# send_mail(
#     "Subject here",
#     "Here is the message.",
#     "jjjhacking@gmail.com",
#     ["eyobjjj@gmail.com"],
#     fail_silently=False,
# )