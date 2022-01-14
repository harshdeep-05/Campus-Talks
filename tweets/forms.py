from django import forms
from django.forms import ModelForm
from .models import Tweet

class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['timestamp', 'like', 'user', 'retweet_status', 'origin_tweet_user', 'parent']
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class' : "form-control", 'maxlength' : 140, 'required': '', 'autofocus':'', 'placeholder' : 'Whats Happening?'}),
        }

class TweetReplyForm(forms.ModelForm):
    class Meta:
        model = Tweet
        exclude = ['timestamp', 'like', 'user', 'retweet_status', 'origin_tweet_user', 'parent', 'content']
