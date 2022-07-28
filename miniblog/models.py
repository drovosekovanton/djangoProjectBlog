from django.db import models
from django.contrib.auth.models import User


class BlogUser(models.Model):
    """
        Users will be added through admin form (for now)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_author = models.BooleanField()
    bio = models.TextField()
    # usage shortcut
    # u = User.objects.get(username='smith')
    # bio = u.blogger.bio

    def __str__(self):
        return self.user.get_full_name()


class Post(models.Model):
    date_published = models.DateTimeField()
    author = models.ForeignKey(BlogUser, on_delete=models.CASCADE)
    post_text = models.TextField()

    def __str__(self):
        return f'{self.author.user.get_full_name()}: {self.post_text[:50]}'


class Comment(models.Model):
    date_published = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField(default='')

    def __str__(self):
        return f'{self.user.get_full_name()}: {self.comment_text[:50]}'
