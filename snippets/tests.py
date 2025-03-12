from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Snippet, Language

class SnippetViewsTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='testuser2', password='testpassword')
        self.language = Language.objects.create(name="Python", slug="python")
        self.snippet = Snippet.objects.create(
            user=self.user,
            name="Test Snippet",
            description="This is a test snippet",
            snippet="print('Hello, World!')",
            language=self.language,
            public=True
        )

    # INDEX
    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Snippet")

    # SNIPPETS ADD
    def test_snippet_add_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('snippet_add'), {
            "name": "New Snippet",
            "description": "Another test snippet",
            "snippet": "print('Hi!')",
            "language": self.language.id,
            "public": True
        })
        self.assertEqual(response.status_code, 302)  # Redirects after creation
        self.assertEqual(Snippet.objects.count(), 2)

    def test_snippet_add_unauthenticated(self):
        response = self.client.get(reverse('snippet_add'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('snippet_add')}")

    # SNIPPETS EDIT
    def test_snippet_edit_owner(self):
        self.client.login(username='testuser', password='testpassword')
        self.client.post(reverse('snippet_edit', args=[self.snippet.id]), {
            "name": "Updated Snippet",
            "description": "Updated description",
            "snippet": "print('Updated!')",
            "language": self.language.id,
            "public": True
        })
        self.snippet.refresh_from_db()
        self.assertEqual(self.snippet.name, "Updated Snippet")

    def test_snippet_edit_not_owner(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('snippet_edit', args=[self.snippet.id]))
        self.assertRedirects(response, reverse('index'))

    # SNIPPETS DELETE
    def test_snippet_delete_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('snippet_delete', args=[self.snippet.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Snippet.objects.filter(id=self.snippet.id).exists())

    def test_snippet_delete_not_owner(self):
        self.client.login(username='testuser2', password='testpassword')
        response = self.client.get(reverse('snippet_delete', args=[self.snippet.id]))
        self.assertRedirects(response, reverse('index'))

    # SNIPPETS DETAILS
    def test_snippet_details_public(self):
        response = self.client.get(reverse('snippet', args=[self.snippet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Snippet")

    def test_snippet_details_private_not_owner(self):
        self.snippet.public = False
        self.snippet.save()
        response = self.client.get(reverse('snippet', args=[self.snippet.id]))
        self.assertRedirects(response, reverse('index'))

    def test_snippet_details_private_owner(self):
        self.snippet.public = False
        self.snippet.save()
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('snippet', args=[self.snippet.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Snippet")

    # USER SNIPPETS 
    def test_user_snippets_owner(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('user_snippets', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Snippet")

    def test_user_snippets_public_only(self):
        self.snippet.public = False
        self.snippet.save()
        response = self.client.get(reverse('user_snippets', args=[self.user.username]))
        self.assertNotContains(response, "Test Snippet")

    # LOGIN TEST
    def test_login_view(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 302)

    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('index'))