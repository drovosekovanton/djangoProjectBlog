A simple blog Django application.

It has no complicated features, just only texting and commenting.

The project was written as the final exam work after my employer's internal Django education. It represents different aspects of working with models and views. Some HTML in templates and CSS are also present. And tests, of course, there are tests.

This blog was inspirited by Mozilla developers' documents site with a DIY project for their Django tutorial. Although my project is not the same thing, they are pretty close enough.

The application relies on the PostgreSQL database. At your local directory, you must have settings_local.py with configured LOCAL_DATABASES, LOCAL_SECRET_KEY, and LOCAL_AUTH_PASSWORD_VALIDATORS variables - they will be imported in the main settings.py script, replacing the original values.

All users created in admin panel with superuser. The permission system relies on two different groups of regular users:
  - Bloggers can write their post and comments on other's posts
  - Commentators can only comment on other's posts

Names of the groups can be different, just make sure that one group can add a comment only, and the other can also add a post, that's all.


Most of the things can be done from the admin panel, including post and comments editing, but this is restricted to admin panels only, regular users can not edit or delete their posts or comments.


As a quick start, in the Django shell you can import and run the _create_test_data_ function from miniblog\tests.py. It will pre-populate the database with bloggers, regular users, their permissions, posts, and comments (users' passwords will be the same as usernames).


Project also has basic API implementation. For now it is restricted with viewing of authors, posts and comments. Neither creating objects, nor updating nor deleting is not supported. API endpoint is available through /miniblog/api url.