A simple blog application written on Django.

It has no complicated features, just only texting and commenting.

Project was written as the final exam work after my employer's internal Django education. It represents different aspects of working with models and views. Some HTML in templates and css are also present.

Blog was inspirated by Mozilla's developers documents site with DIY project for their Django tutorial. Although my project is not really the same thing, they are pretty close enough.

Application relies on PostgreSQL database. At your local directory you must have settings_local.py with configured LOCAL_DATABASES, LOCAL_SECRET_KEY and LOCAL_AUTH_PASSWORD_VALIDATORS variables - they will be importing in main settings.py script, replacing original values.

All users created in admin panel with superuser. Permission system relies on two different groups for regular users:
  - Bloggers can wright their post and comments other's posts
  - Commenters can only comment other's posts

Names of groups can be different, just make sure that one group can add comment only, and the other can also add post, that's all.
