from django.shortcuts import get_object_or_404, render, redirect

from django.urls import reverse_lazy

from django.views.generic import FormView, DeleteView

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User

from django.core.paginator import Paginator

from django.db.models import Q

from django.forms import forms
from .forms import GroupCheckboxForm, GroupSelectMenuForm, FriendsCheckboxForm, CreateGroupForm, PostForm, SearchForm
from .models import Post, Group, Friend, Good

from django.db.utils import IntegrityError

# Create your views here.


# 全員が見れるページの作成者であるsampleユーザーとそのグループを取得する
def get_public_user_group():
    public_user = User.objects.filter(username='sample').first()
    public_group = Group.objects.filter(group_owner_id=public_user).first()
    return (public_user, public_group)


def get_search_group_post(user, group_list, search, page):
    page_num = 5
    
    # 全員が見れるページの作成者であるsampleユーザーとそのグループを取得する
    (public_user, public_group) = get_public_user_group()
    
    # 指定されたグループの取得
    selected_groups = Group.objects.filter(group_name__in=group_list)
    
    # 指定されたグループから全ての投稿を取得
    posts = Post.objects.filter(group_id__in=selected_groups).filter(content__icontains=search).order_by('-created_at')
    
    # print('--------posts--------')
    # print(posts)
    
    # ページネーション
    page_item = Paginator(posts, page_num)
    # print('--------page_item--------')
    # print(page_item)
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
        searchform = SearchForm(request.POST)
        search = request.POST['search'] 
        # チェックされたグループ名をリストにまとめる
        group_name_list = []
        for group in request.POST.getlist('groups'):
            group_name_list.append(group)
        #     print('-------group---')
        #     print(group)
        # print('-------group_name_list---')
        # print(group_name_list)
        # 投稿の取得
        posts = get_search_group_post(request.user, group_name_list, search, page)
        # print('-------posts---')
        # print(posts)
        
        
    # GET
    else:
        # フォームの用意
        checkform = GroupCheckboxForm(request.user)
        searchform = SearchForm()
        # print('-------checkform-------')
        # print(checkform)
        # グループのリストを取得
        groups = Group.objects.filter(group_owner_id=request.user)
        group_name_list = []
        for group in groups:
            group_name_list.append(group.group_name)
        # 投稿の取得
        posts = get_search_group_post(request.user, group_name_list, '', page)
        
    params = {
        'login_user':request.user,
        'contents':posts,
        'check_form':checkform,
        'search_form':searchform,
    }
    return render(request, 'Chirp/home.html', params)

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
    
    messages.success(request, add_user.username + ' を追加しました！')
    return redirect(to='/')

# グループ作成処理
@login_required
def create_group(request):
    if request.method == 'POST':
        # 送信内容の取得
        group_name = request.POST['group_name']
        # グループの保存
        group = Group()
        group.group_owner_id = request.user
        group.group_name = request.user.username + 'の' + request.POST['group_name']
        group.save()
        messages.success(request, '新しいグループを作成しました！')
        return redirect(to='/')
        
    createform = CreateGroupForm()
    params = {
        'login_user' : request.user,
        'create_form' : createform,
    }
    
    return render(request, 'Chirp/create_group.html', params)


# 投稿処理
@login_required
def post(request):
    # POST
    if request.method == 'POST':
        # 送信内容の取得
        group_id = request.POST['groups']
        content = request.POST['content']
        # グループの取得
        group = Group.objects.get(id=group_id)
        if group == None:
            (public_user, group) = get_public_user_group()
        # 投稿の保存
        # print('-------投稿先のグループ-------')
        # print(group)
        # print('-----------------------')
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
        group_id = request.POST['groups'] 
        content = request.POST['content']
        
        # グループの取得
        group = Group.objects.get(id=group_id)
        if group == None:
            (public_user, group) = get_public_user_group()
        # 投稿を作成
        post = Post()
        post.contributor_id = request.user
        post.group_id = group
        post.content = content
        post.share_id = share.id
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
        messages.success(request, '既にこのメッセージには"いいね！"済みです')
        return redirect(to='/')

    # goodする投稿のgood_countを1増やす
    good_post.good_count += 1
    good_post.save()
    # goodの保存
    good = Good()
    good.good_user_id = request.user
    good.good_post_id = good_post
    good.save()
    
    messages.success(request, '投稿に"いいね！"しました!')
    return redirect(to='/')

# 自分の投稿の削除
@login_required
def mypost_delete(request, post_id):
    # 投稿の取得
    post = get_object_or_404(Post, id=post_id, contributor_id=request.user)

    if request.method == 'POST':
        post.delete()
        
        messages.success(request, '投稿を削除しました！')
        return redirect('home')
    else:
        params = {
            'login_user' : request.user,
            'post' : post,
        }
        return render(request, 'Chirp/mypost_delete.html', params)