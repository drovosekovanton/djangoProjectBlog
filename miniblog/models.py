from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class BlogUser(models.Model):
    """
        Users will be added through admin form (for now)
        BlogUser is an additional object to built-in User model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.user.username


class Post(models.Model):
    """
        A single Post object represents one post from specific blogger
    """
    date_published = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_title = models.CharField(max_length=250)
    post_text = models.TextField()

    def __str__(self):
        return f'{self.user.username}: {self.post_title[:50]}'

    def get_absolute_url(self):
        return reverse('post', kwargs={'pk': self.pk})


class Comment(models.Model):
    """
        Comment model represents a comment to the specific post
    """
    date_published = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()

    def __str__(self):
        return f'{self.user.username}: {self.comment_text[:50]}'
