from django.shortcuts import render, redirect

from django.urls import reverse_lazy

from django.views.generic import FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.models import User

from django.core.paginator import Paginator

from django.db.models import Q

from django.forms import forms
from .forms import GroupCheckboxForm, GroupSelectMenuForm, FriendsCheckboxForm, CreateGroupForm, PostForm
from .models import Post, Group, Friend, Good

# Create your views here.


# 全員が見れるページの作成者であるsampleユーザーとそのグループを取得する
def get_public_user_group():
    public_user = User.objects.filter(username='sample').first()
    public_group = Group.objects.filter(group_owner_id=public_user).first()
    return (public_user, public_group)


def get_search_group_post(user, group_list, page):
    page_num = 10
    
    # 全員が見れるページの作成者であるsampleユーザーとそのグループを取得する
    (public_user, public_group) = get_public_user_group()
    
    # 指定されたグループの取得する
    groups = Group.objects.filter(Q(group_owner_id=user) | Q(group_owner_id=public_user)).filter(group_name__in=group_list)
    # そのグループに含まれるフレンドの取得
    me_friends = Friend.objects.filter(group_id__in=groups)
    # フレンドのユーザーIDの取得してリストにまとめておく
    me_users = []
    for me_friend in me_friends:
        me_users.append(me_friend.user_id)
    
    # リスト内のユーザーが作ったグループの取得
    his_groups = Group.objects.filter(group_owner_id__in=me_users)
    his_friends = Friend.objects.filter(user_id=user).filter(group_id__in=his_groups)
    
    me_groups = []
    for his_friend in his_friends:
        me_groups.append(his_friend.group_id)
    
    # group_idがgroupsかme_groupsに含まれるpostを取得する
    posts = Post.objects.filter(Q(group_id__in=groups) | Q(group_id__in=me_groups))
    
    # ページネーション
    page_item = Paginator(posts, page_num)
    return page_item.get_page(page)
 

class LoginView(LoginView):
    template_name = "Chirp/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("home")
    
class SignupView(FormView):
    template_name = "Chirp/signup.html"
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("home")
        return super(SignupView, self).get(*args, **kwargs)


@login_required
def home(request, page=1):
    # 全員が見れるページの作成者であるsampleユーザーとそのグループを取得する
    (public_user, public_group) = get_public_user_group()
    
    # POST
    if request.method == 'POST':
        
        # フォームの用意
        checkform = GroupCheckboxForm(request.user, request.POST)
        # チェックされたグループ名をリストにまとめる
        group_name_list = []
        for group in request.POST.getlist('groups'):
            group_name_list.append(group)
        # 投稿の取得
        posts = get_search_group_post(request.user, group_name_list, page)
        
    # GET
    else:
        # フォームの用意
        checkform = GroupCheckboxForm(request.user)
        # グループのリストを取得
        groups = Group.objects.filter(group_owner_id=request.user)
        group_name_list = []
        for group in groups:
            group_name_list.append(group.group_name)
        # 投稿の取得
        posts = get_search_group_post(request.user, group_name_list, page)
        
    params = {
        'login_user':request.user,
        'contents':posts,
        'check_form':checkform,
    }
    return render(request, 'Chirp/home.html', params)

@login_required
def groups(request):
    # 自分のフレンとの取得
    friends = Friend.objects.filter(friend_owner_id=request.user)
    
    # POST
    if request.method == 'POST':
        
        # グループメニュー
        if request.POST['mode'] == '__groups_form__':
            # 選択したグループ名を取得
            select_group = request.POST['groups']
            # グループを取得
            group = Group.objects.filter(group_owner_id=request.user).filter(group_name=select_group).first()
            # グループに含まれるフレンドを取得
            friends = Friend.objects.filter(friend_owner_id=request.user).filter(group_id=group)
            print(Friend.objects.filter(friend_owner_id=request.user))
            # フレンドのユーザーIDをリストにまとめる
            friends_list = []
            for friend in friends:
                friends_list.append(friend.user_id.username)
                
            # フォームの用意
            groupsform = GroupSelectMenuForm(request.user, request.POST)
            friendsform = FriendsCheckboxForm(request.user, friends=friends, vals=friends_list)
            
        # フレンドのチェック更新時
        if request.POST['mode'] == '__friends_form__':
            # 選択したグループの取得
            select_group = request.POST['group']
            group_obj = Group.objects.filter(group_name=select_group).first()
            print(group_obj)
            # チェックしたフレンドを取得
            select_friends = request.POST.getlist('friends')
            # フレンドのユーザー取得
            select_users = User.objects.filter(username__in=select_friends)
            # Userに含まれるユーザーが登録したフレンドを取得
            friends = Friend.objects.filter(friend_owner_id__in=select_users).filter(group_id=group_obj)
            
            # フレンド全員にグループを設定して保存
            friends_list = []
            for friend in friends:
                friend.group_id = group_obj
                friend.save()
                friends_list.append(friend.user_id.username)
            
            messages.success(request, 'チェックされたFriendを' + select_group + 'に登録しました!')
            
            # フォームの用意
            groupsform = GroupSelectMenuForm(request.user, {'groups':select_group})
            friendsform = FriendsCheckboxForm(request.user, friends=friends, vals=friends_list)
            
    # GET
    else:
        # フォームの用意
        groupsform = GroupSelectMenuForm(request.user)
        friendsform = FriendsCheckboxForm(request.user, friends=friends, vals=[])
        select_group = '-'
        
    createform = CreateGroupForm()
    params = {
        'login_user' : request.user,
        'groups_form' : groupsform,
        'friends_form' : friendsform,
        'create_form' : createform,
        'group' : select_group,
    }
    return render(request, 'Chirp/groups.html', params)


# フレンドの追加処理
@login_required
def add(request):
    # 追加するユーザーを取得
    add_name = request.GET['name']
    add_user = User.objects.filter(username=add_name).first()
    # ユーザーが本人の場合
    if add_user == request.user:
        messages.info(request, '自分自身をFriendに追加することはできません。')
        return redirect(to='/')

    # publicの取得
    (public_user, public_group) = get_public_user_group()
    
    # add_userのフレンドの数を調べる
    friend_num = Friend.objects.filter(friend_owner_id=request.user).filter(user_id=add_user).count()
    # ゼロより大きければ既に登録済み
    if friend_num > 0:
        messages.info(request, add_user.username + ' は既に追加されています。')
        return redirect(to='/')

    # フレンドの登録処理
    friend = Friend()
    friend.friend_owner_id = request.user
    friend.user_id = add_user
    friend.group_id = public_group
    friend.save()
    
    messages.success(request, add_user.username + ' を追加しました！groupページに移動して、追加したFriendをメンバーに設定してください。')
    return redirect(to='/')

# グループ作成処理
@login_required
def create_group(request):
    group = Group()
    group.group_owner_id = request.user
    group.group_name = request.user.username + 'の' + request.POST['group_name']
    group.save()
    messages.success(request, '新しいグループを作成しました！')
    return redirect(to='/groups')


# 投稿処理
@login_required
def post(request):
    # POST
    if request.method == 'POST':
        # 送信内容の取得
        group_name = request.POST['groups']
        content = request.POST['content']
        # グループの取得
        group = Group.objects.filter(group_owner_id=request.user).filter(group_name=group_name).first()
        if group == None:
            (public_user, group) = get_public_user_group()
        # 投稿の保存
        post = Post()
        post.contributor_id = request.user
        post.group_id = group
        post.content = content
        post.save()
        
        messages.success(request, '投稿しました！')
        return redirect(to='/')
    
    # GET
    else:
        form = PostForm(request.user)
        
    params = {
        'login_user' : request.user,
        'form' : form,
    }
    return render(request, 'Chirp/post.html', params)

# 投稿のシェア
@login_required
def share(request, share_id):
    # シェアする投稿の取得
    share = Post.objects.get(id=share_id)
    print(share)
    
    # POST
    if request.method == 'POST':
        group_name = request.POST['groups']
        content = request.POST['content']
        # グループの取得
        group = Group.objects.filter(group_owner_id=request.user).filter(group_name=group_name).first()
        if group == None:
            (public_user, group) = get_public_user_group()
        # 投稿を作成
        post = Post()
        post.contributor_id = request.user
        post.group_id = group
        post.content = content
        post.share_id = share
        post.save()
        share_message = post.get_share()
        share_message.shared_count += 1
        share_message.save()
        
        messages.success(request, '投稿をシェアしました！')
        return redirect(to='/')

    form = PostForm(request.user)
    params = {
        'login_user' : request.user,
        'form' : form,
        'share' : share,
    }
    return render(request, 'Chirp/share.html', params)

# goodボタンの処理
@login_required
def good(request, good_id):
    # goodする投稿を取得
    good_post = Post.objects.get(id=good_id)
    # 自分がgoodした数を調べる
    is_good = Good.objects.filter(good_user_id=request.user).filter(good_post_id=good_post).count()
    # ゼロより大きければ既にgood済み
    if is_good > 0:
        messages.success(request, '既にメッセージにはGoodしています。')
        return redirect(to='/')

    # goodする投稿のgood_countを1増やす
    good_post.good_count += 1
    good_post.save()
    # goodの保存
    good = Good()
    good.good_user_id = request.user
    good.good_post_id = good_post
    good.save()
    
    messages.success(request, '投稿にGoodしました！')
    return redirect(to='/')