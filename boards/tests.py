from django.test import TestCase
from django.urls import reverse,resolve
from .views import home
from .models import Board
# Create your tests here.
class HomeTests(TestCase):
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

    