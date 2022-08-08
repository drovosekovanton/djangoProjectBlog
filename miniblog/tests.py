from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from .models import Post, Comment, BlogUser

from random import randint, random, choice
from faker import Faker
from datetime import timedelta


def create_test_data():
    number_of_posts = 20
    number_of_bloggers = 7
    number_of_commentators = 10
    max_number_of_comments = 20
    fake_factory = Faker()

    # creating test groups
    Group.objects.create(name='Bloggers')
    Group.objects.create(name='Commentators')

    # create test permissions
    contenttype = ContentType.objects.get(app_label='miniblog', model='post')
    permission = Permission.objects.get(
        codename='add_post',
        content_type=contenttype,
    )
    Group.objects.get(name='Bloggers').permissions.add(permission)

    contenttype = ContentType.objects.get(app_label='miniblog', model='comment')
    permission = Permission.objects.get(
        codename='add_comment',
        content_type=contenttype,
    )
    Group.objects.get(name='Bloggers').permissions.add(permission)
    Group.objects.get(name='Commentators').permissions.add(permission)

    # create test users: bloggers and commentators
    group = Group.objects.get(name='Bloggers')
    for index in range(number_of_bloggers):
        u = User.objects.create_user(
            username=f'blogger_{index}',
            password=f'blogger_{index}',
        )
        if random() > 0.5:
            BlogUser.objects.create(
                user=u,
                bio=fake_factory.text(max_nb_chars=100),
            )
        u.groups.add(group)

    group = Group.objects.get(name='Commentators')
    for index in range(number_of_commentators):
        u = User.objects.create_user(
            username=f'commentator_{index}',
            password=f'commentator_{index}',
        )
        u.groups.add(group)

    # create test posts with optional comments
    for index in range(number_of_posts):
        p = Post(
            post_title=fake_factory.text(max_nb_chars=250),
            post_text=fake_factory.text(max_nb_chars=1000),
            user=choice(User.objects.filter(username__startswith='blogger')),
            date_published=timezone.make_aware(
                fake_factory.date_time_between_dates(
                    timezone.now() - timedelta(30),
                    timezone.now(),
                )
            ),
        )
        p.save()
        for _ in range(randint(0, max_number_of_comments)):
            Comment.objects.create(
                user=choice(User.objects.all()),
                date_published=timezone.make_aware(
                    fake_factory.date_time_between_dates(
                        p.date_published,
                        timezone.now()),
                ),
                post=p,
                comment_text=fake_factory.sentence(nb_words=10),
            )


class TestMix(TestCase):

    @classmethod
    def setUpTestData(cls):
        create_test_data()

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/miniblog/posts/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'miniblog/post_all.html')

    def test_pagination_is_five(self):
        resp = self.client.get(reverse('posts'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] is True)
        self.assertEqual(len(resp.context['page_obj']), 5)
        self.assertEqual(len(resp.context['post_list']), 5)

    def test_wrong_post_index(self):
        # post index farther than max test posts count
        resp = self.client.get(reverse('post', kwargs={'pk': 100}))
        self.assertEqual(resp.status_code, 404)

    def test_commentator_can_not_post(self):
        c = self.client
        resp = c.post(
            reverse('login'),
            {'username': 'commentator_0', 'password': 'commentator_0'},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        resp = c.get(reverse('create_post'), follow=True)
        self.assertEqual(resp.status_code, 403)

    def test_anonymous_redirects_to_login_in_comments(self):
        from django.contrib.auth.views import LoginView
        resp = self.client.get(reverse('create_comment', kwargs={'pk': Post.objects.first().pk}), follow=True)
        self.assertIsInstance(resp.context_data['view'], LoginView)

    def test_anonymous_redirects_to_login_in_create_post(self):
        from django.contrib.auth.views import LoginView
        resp = self.client.get(reverse('create_post'), follow=True)
        self.assertIsInstance(resp.context_data['view'], LoginView)

    def test_no_empty_post(self):
        c = self.client
        resp = c.post(
            reverse('login'),
            {'username': 'blogger_0', 'password': 'blogger_0'},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        resp = c.post(
            reverse('create_post'),
            {'post_title': '',
             'post_text': ''},
            follow=True,
        )
        # we stays on the same page
        self.assertEqual(resp.request['PATH_INFO'], reverse('create_post'))

    def test_no_empty_comments(self):
        c = self.client
        resp = c.post(
            reverse('login'),
            {'username': 'commentator_0', 'password': 'commentator_0'},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        resp = c.post(
            reverse('create_comment', kwargs={'pk': Post.objects.first().pk}),
            {'comment_text': ''},
        )
        # we stays on the same page
        self.assertEqual(
            resp.request['PATH_INFO'],
            reverse('create_comment', kwargs={'pk': Post.objects.first().pk})
        )
