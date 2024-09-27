from django.test import TestCase
from django.urls import reverse,resolve
from .views import home,board_topics,new_topic
from django.contrib.auth.models import User
from .forms import NewTopicForm
from .models import Board, Post, Topic

class HomeTests(TestCase):
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_home_view_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEqual(view.func, home)

    def test_home_view_args(self):
        boards = Board.objects.all()
        response = self.client.get(reverse('home'))
        self.assertIn('boards', response.context)
        context_boards = response.context['boards']
        self.assertEqual(list(context_boards), list(boards))

    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))
