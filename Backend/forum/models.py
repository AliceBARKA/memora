from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class ForumPost(models.Model):
    CATEGORY_CHOICES=[
        ("question","Qustions"),
        ("help","Aide"),
        ("course","Cours"),
        ("general","General"),
    ]

    title =models.CharField(max_length=255)
    content =models.TextField()
    category=models.CharField(max_length=20,choices=CATEGORY_CHOICES,default="general")
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name="forum_posts")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.title
    
class   ForumComment(models.Model):
    post=models.ForeignKey(ForumPost,on_delete=models.CASCADE,related_name="comments")
    author=models.ForeignKey(User,on_delete=models.CASCADE,related_name="forum_comments")
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"
    
    