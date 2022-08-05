# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from .models import BlogUser


# In this project, 'Bio' field of user will be populated through admin interface only

# @receiver(post_save, sender=User)
# def update_bloguser(sender, **kwargs):
#     """
#         after creating a new user inserts corresponding bloguser record
#     """
#     if kwargs['created']:
#         # we should create BlogUser record to new user
#         BlogUser.objects.create(user=kwargs['instance'], Bio='smth')
