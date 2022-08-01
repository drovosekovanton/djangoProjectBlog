from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class BlogUser(models.Model):
    """
        Users will be added through admin form (for now)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_author = models.BooleanField()
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    date_published = models.DateTimeField()
    blog_user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=250)
    post_text = models.TextField()

    def __str__(self):
        return f'{self.blog_user.user.username}: {self.post_title[:50]}'

    # def get_absolute_url(self):
    #     return reverse('posts')  #, args=[self.id])


class Comment(models.Model):
    date_published = models.DateTimeField()
    blog_user = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return f'{self.blog_user.user.username}: {self.comment_text[:50]}'
