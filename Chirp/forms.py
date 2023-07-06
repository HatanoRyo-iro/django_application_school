from django import forms
from django.contrib.auth.models import User

from .models import Post, Group, Friend, Good


# 投稿フォーム
class PostForm(forms.ModelForm):
    content = forms.CharField(label='投稿', max_length=280, widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' : 2}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.get(username='public').first()
        self.field['groups'] = forms.ChoiceField(choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(owner__in=[user, public])],
                                                 widget=forms.Select(attrs={'class' : 'form-control'}))