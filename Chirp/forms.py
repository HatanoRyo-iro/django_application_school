from django import forms
from django.contrib.auth.models import User

from .models import Post, Group, Friend, Good


# グループチェックボックスフォーム
class GroupCheckboxForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckboxForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='sample').first()
        self.fields['groups'] = forms.MultipleChoiceField(choices=[(item.group_name, item.group_name) for item in Group.objects.filter(group_owner_id__in=[user, public])],
                                                          widget = forms.CheckboxSelectMultiple(attrs={'class' : 'form-check-input'}))


# グループ選択メニューフォーム
class GroupSelectMenuForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupSelectMenuForm, self).__init__(*args, **kwargs)
        self.fields['groups'] = forms.ChoiceField(choices=[('-', '-')] + [(item.group_name, item.group_name) for item in Group.objects.filter(group_owner_id=user)],
                                                  widget=forms.Select(attrs={'class' : 'form-control'}))


# フレンドのチェックボックスフォーム
class FriendsCheckboxForm(forms.Form):
    def __init__(self, user, friends=[], vals=[], *args, **kwargs):
        super(FriendsCheckboxForm, self).__init__(*args, **kwargs)
        self.friends['friends'] = forms.MultipleChoiceField(choices=[(item.user_id, item.user_id) for item in friends],
                                                            widget=forms.CheckboxSelectMultiple(attrs={'class' : 'form-check-input'}), initial=vals)
    
    
# グループ作成フォーム
class CreateGroupForm(forms.ModelForm):
    group_name = forms.CharField(label='グループ名', max_length=50, 
                                   widget=forms.TextInput(attrs={'class' : 'form-control'}))

# 投稿フォーム
class PostForm(forms.ModelForm):
    content = forms.CharField(label='投稿', max_length=280, widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' : 2}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.get(username='sample').first()
        self.field['groups'] = forms.ChoiceField(choices=[('-', '-')] + [(item.title, item.title) for item in Group.objects.filter(group_owner_id__in=[user, public])],
                                                 widget=forms.Select(attrs={'class' : 'form-control'}))