from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse, resolve
from ..models import Board, Post, Topic
from ..views import reply_topic

class ReplyTopicTestCase(TestCase):
    '''
    Base test case to be used in all `reply_topic` view tests
    '''
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        self.username = 'john'
        self.password = '123'
        user = User.objects.create_user(username=self.username, email='john@doe.com', password=self.password)
        self.topic = Topic.objects.create(subject='Hello, world', board=self.board, starter=user)
        Post.objects.create(message='Lorem ipsum dolor sit amet', topic=self.topic, created_by=user)
        self.url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})

class LoginRequiredReplyTopicTests(ReplyTopicTestCase):
    def test_redirection(self):
        '''
        Test if a non-logged-in user is redirected to the login page
        '''
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/login/?next={self.url}')


class ReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_reply_topic_view_success_status_code(self):
        '''
        Test if the reply_topic view returns a 200 status code for logged-in users
        '''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_reply_topic_view_not_found_status_code(self):
        '''
        Test if the view returns a 404 status code when the topic does not exist
        '''
        url = reverse('reply_topic', kwargs={'pk': self.board.pk, 'topic_pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_reply_topic_url_resolves_reply_topic_view(self):
        '''
        Test if the URL for reply_topic resolves to the correct view function
        '''
        view = resolve(self.url)
        self.assertEqual(view.func, reply_topic)

class SuccessfulReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)
        self.data = {
            'message': 'This is a test message.'
        }

    def test_valid_reply_topic_post_data(self):
        '''
        Test if a valid form submission creates a new post and redirects
        '''
        response = self.client.post(self.url, self.data)
        self.assertEqual(Post.objects.count(), 2)
        self.assertRedirects(response, reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk}))

    def test_valid_reply_topic_post_data_redirect(self):
        '''
        Test if a valid form submission redirects to the correct topic page
        '''
        response = self.client.post(self.url, self.data)
        topic_posts_url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        self.assertRedirects(response, topic_posts_url)

    def test_redirection(self):
        '''
        A valid form submission should redirect the user
        '''
        url = reverse('topic_posts', kwargs={'pk': self.board.pk, 'topic_pk': self.topic.pk})
        topic_posts_url = '{url}?page=1#2'.format(url=url)
        self.assertRedirects(self.response, topic_posts_url)

class InvalidReplyTopicTests(ReplyTopicTestCase):
    def setUp(self):
        super().setUp()
        self.client.login(username=self.username, password=self.password)

    def test_invalid_reply_topic_post_data(self):
        '''
        Test if an invalid form submission doesn't create a new post
        '''
        response = self.client.post(self.url, {'message': ''})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Post.objects.filter(message='').exists())
