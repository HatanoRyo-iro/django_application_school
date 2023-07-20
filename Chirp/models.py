from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    contributor_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_id = models.ForeignKey('Group', on_delete=models.CASCADE)
    content = models.TextField(max_length=280)
    share_id = models.IntegerField(default=-1) 
    good_count = models.IntegerField(default=0)
    shared_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.content
    
    def get_share(self):
        return Post.objects.get(id=self.share_id)
    
    class Meta:
        ordering = ('-created_at',)
        
        
class Group(models.Model):
    group_owner_id = models.ForeignKey(User, on_delete=models.CASCADE)
    group_name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.group_name + '(' + str(self.group_owner_id) +')'
    
    
class Friend(models.Model):
    friend_owner_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_owner')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_user')
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.user_id) + '(group:"' + str(self.group_id) + '")'
    
    
class Good(models.Model):
    good_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    good_post_id = models.ForeignKey(Post, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'good "' + str(self.good_post_id) + '" by ' + str(self.good_user_id)

    
