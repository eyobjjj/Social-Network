from django import forms

from .models import Post, ChatMassage, UserProfile
from django.contrib.auth.models import User

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border text-black'

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

        widgets = {
            'username': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'first_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'last_name': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'email': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            })
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user','bio','profileimg','location')

        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full h-28 rounded-xl border text-black'
            }),
            'location': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'profileimg': forms.FileInput(attrs={
                'class': INPUT_CLASSES
            })
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('catagory','image','description')

        widgets={
            'catagory' : forms.Select(attrs={
            }),
            'description' : forms.TextInput(attrs={
                'placeholder':'descriptions',
            })
        }


class ChatMassageForm(forms.ModelForm):
    class Meta:
        model = ChatMassage
        fields = ('massage', 'file',)

        widgets={
            'massage' : forms.TextInput(attrs={
                'placeholder':'Type your message...',
                'class':'w-full border rounded-full py-2 px-4 mr-2'
            })
        }


