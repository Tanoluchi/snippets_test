from django.shortcuts import get_object_or_404, redirect, render
from django.utils.decorators import method_decorator
from django.contrib.auth import login, logout
from django.db.models import Q
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

from .forms import SnippetForm
from .tasks import sendEmailInSnippetCreation
from .utils import is_the_owner
from .decorators import owner_required

from .models import (
    Snippet,
    Language,
    User
)

class SnippetAdd(LoginRequiredMixin, View):
    """
    View to add a new snippet.
    
    GET: Renders a form for creating a new snippet.
    POST: Processes the form data, creates a snippet associated with the current user, 
          and redirects to the snippet detail view if successful.
    """

    def get(self, request, *args, **kwargs):
        form = SnippetForm()
        return render(
            request, 
            "snippets/snippet_add.html", 
            {
                "action": "Add",
                "form": form,
            }
        )
    
    def post(self, request, *args, **kwargs):
        form = SnippetForm(request.POST)
        if form.is_valid():
            snippet = form.save(commit=False)
            snippet.user = request.user
            snippet.save()
            sendEmailInSnippetCreation.delay(snippet.name, snippet.description, snippet.user.email)
            return redirect("snippet", id=snippet.id)
        return render(
            request, 
            "snippets/snippet_add.html", 
            {
                "form": form, 
                "action": "Add"
            }
        )

@method_decorator(owner_required, name="dispatch")
class SnippetEdit(LoginRequiredMixin, View):
    """
    View to edit an existing snippet.
    
    Only the owner of the snippet is allowed to edit it.
    
    GET: Renders a form pre-populated with the snippet's current data.
    POST: Processes the form data and updates the snippet if the data is valid.
    """
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"])
        form = SnippetForm(instance=snippet)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=self.kwargs["id"])
        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("snippet", id=snippet.id)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

@method_decorator(owner_required, name="dispatch")
class SnippetDelete(LoginRequiredMixin, View):
    """
    View to delete a snippet.
    
    Only the owner of the snippet is allowed to delete it.
    
    GET: Deletes the snippet immediately and redirects to the user's snippets list.
    """
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        snippet.delete()
        return redirect("user_snippets", username=request.user.username)

class SnippetDetails(View):
    """
    View to display the details of a snippet.
    
    GET: Renders the snippet detail page. If the snippet is private, only the owner can view it.
    """
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        snippet = get_object_or_404(Snippet, id=snippet_id)
        is_owner = is_the_owner(request, snippet.user.username)
        if not snippet.public and not is_owner:
            return redirect("index")

        return render(
            request, 
            "snippets/snippet.html", 
            {
                "snippet": snippet, 
                "highlighted_snippet": snippet.highlight
            }
        )

class UserSnippets(View):
    """
    View to list all snippets for a given user.
    
    GET: Displays all snippets for the owner if the current user is the owner; 
         otherwise, only displays public snippets.
    """
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        owner = get_object_or_404(User, username=username)
        is_owner = is_the_owner(request, owner.username)
        if is_owner:
            snippets = Snippet.objects.filter(user=owner)
        else:
            snippets = Snippet.objects.filter(user=owner, public=True)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": owner, "snippets": snippets},
        )

class SnippetsByLanguage(View):
    """
    View to list all public snippets for a specific programming language.
    
    GET: Filters snippets by the language slug provided in the URL and renders them in the index template.
    """
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        language_obj = get_object_or_404(Language, slug=language)
        snippets = Snippet.objects.filter(public=True, language=language_obj)
        return render(request, "index.html", {"snippets": snippets})


class Login(AuthenticationForm, View):
    """
    View to handle user authentication.
    
    GET: Displays the login form.
    POST: Authenticates the user using the provided credentials. 
        If successful, logs in the user and redirects to the index page; 
        otherwise, re-renders the login form with errors.
    """
    def get(self, request, *args, **kwargs):
        form = AuthenticationForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.GET.get('next') or 'index'
            return redirect(next_url)
        return render(request, 'login.html', {'form': form})

class Logout(View):
    """
    View to handle user logout.

    GET: Log out the current authenticated user and redirects to the index page.
    """
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('index')

class Index(View):
    """
    View to display the index page with all public snippets.

    GET:
        Retrieves all Snippet objects that are marked as public and renders them
        in the 'index.html' template. 
        If there is an authenticated user, I also look for his snippets to show.
    """
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            snippets = Snippet.objects.filter(
                Q(public=True) | Q(user=request.user)
            ).distinct()
        else:
            snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})