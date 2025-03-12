from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.contrib.auth import login, logout
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import AuthenticationForm

from .forms import SnippetForm
from .tasks import sendEmailInSnippetCreation

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
            # sendEmailInSnippetCreation.delay(snippet.name, snippet.description, snippet.user.email)
            return redirect("snippet", id=snippet.id)
        return render(request, "snippets/snippet_add.html", {"form": form})

class SnippetEdit(LoginRequiredMixin, View):
    """
    View to edit an existing snippet.
    
    Only the owner of the snippet is allowed to edit it.
    
    GET: Renders a form pre-populated with the snippet's current data.
    POST: Processes the form data and updates the snippet if the data is valid.
    """
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        if request.user != snippet.user:
            raise PermissionDenied("No tienes permiso para editar este snippet.")

        form = SnippetForm(instance=snippet)
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

    def post(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        if request.user != snippet.user:
            raise PermissionDenied("No tienes permiso para editar este snippet.")

        form = SnippetForm(request.POST, instance=snippet)
        if form.is_valid():
            form.save()
            return redirect("snippet_detail", id=snippet.id)  # Redirige a la vista del snippet
        return render(request, "snippets/snippet_add.html", {"form": form, "action": "Edit"})

class SnippetDelete(LoginRequiredMixin, View):
    """
    View to delete a snippet.
    
    Only the owner of the snippet is allowed to delete it.
    
    GET: Deletes the snippet immediately and redirects to the user's snippets list.
    """
    def get(self, request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        username = request.user.username
        if username != snippet.user.username:
            raise PermissionDenied("No tienes permiso para eliminar este snippet.")

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
        username = request.user.username
        if not snippet.public and (not request.user.is_authenticated or username != snippet.user.username):
            raise PermissionDenied("No tienes permiso para ver este snippet.")

        return render(request, "snippets/snippet.html", {"snippet": snippet})

class UserSnippets(View):
    """
    View to list all snippets for a given user.
    
    GET: Displays all snippets for the owner if the current user is the owner; 
         otherwise, only displays public snippets.
    """
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        owner = get_object_or_404(User, username=username)
        if request.user.username == owner.username:
            snippets = Snippet.objects.filter(user=owner)
        else:
            snippets = Snippet.objects.filter(user=owner, public=True)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
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


# class Login(View):
#    TODO: Implement login view logic with AuthenticationForm and login handling.

# class Logout(View):
#    TODO: Implement logout view logic.

class Index(View):
    """
    View to display the index page with all public snippets.

    GET:
        Retrieves all Snippet objects that are marked as public and renders them
        in the 'index.html' template.
    """
    def get(self, request, *args, **kwargs):
        snippets = Snippet.objects.filter(public=True)
        return render(request, "index.html", {"snippets": snippets})