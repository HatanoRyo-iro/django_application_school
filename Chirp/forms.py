from django import forms
from django.contrib.auth.models import User

from .models import Post, Group, Friend, Good




# グループチェックボックスフォーム
class GroupCheckboxForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(GroupCheckboxForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='sample').first()
        print('--------public--------')
        print(public)
        my_friend = Friend.objects.filter(friend_owner_id_id=user.id)
        print('--------friend--------')
        print(my_friend)
        friends_ids = [item.user_id for item in my_friend]
        self.fields['groups'] = forms.MultipleChoiceField(choices=[(item.group_name, item.group_name) for item in Group.objects.filter(group_owner_id__in=[user, *friends_ids, public])],
                                                          widget = forms.CheckboxSelectMultiple(), error_messages={'required': '1つ以上選択してください'})


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
        self.fields['friends'] = forms.MultipleChoiceField(choices=[(item.user_id, item.user_id) for item in friends],
                                                            widget=forms.CheckboxSelectMultiple(), initial=vals)


# グループ作成フォーム
class CreateGroupForm(forms.Form):
    group_name = forms.CharField(label='グループ名', max_length=50,
                                   widget=forms.TextInput(attrs={'class' : 'form-control'}))

# 投稿フォーム
class PostForm(forms.Form):
    content = forms.CharField(label='投稿', max_length=280, widget=forms.Textarea(attrs={'class' : 'form-control', 'rows' : 2}))
    
    def __init__(self, user, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        public = User.objects.filter(username='sample').first()
        my_friends = Friend.objects.filter(friend_owner_id_id=user.id)
        my_friends_groups = Group.objects.filter(group_owner_id__in=my_friends.values('user_id'))
        print('--------my_friends_groups--------')
        print(my_friends_groups)
        print('---------------------------------')
        my_friends_groups_ids = [item.id for item in my_friends_groups]
        print('--------my_friends_groups_ids--------')
        print(my_friends_groups_ids)
        print('---------------------------------')
        self.fields['groups'] = forms.ChoiceField(choices=[('-', '-')] + [(item.id, item.group_name) for item in Group.objects.filter(group_owner_id__in=[user, *my_friends_groups_ids, public])],
                                                 widget=forms.Select(attrs={'class' : 'form-control'}))
        
    