from django.shortcuts import render
from django.views import View


# class SnippetAdd(View):
#    TODO: Implement this class to handle snippet creation, only for authenticated users.

# class SnippetEdit(View):
#    TODO: Implement this class to handle snippet editing. Allow editing only for the owner.

# class SnippetDelete(View):
#    TODO: Implement this class to handle snippet deletion. Allow deletion only for the owner.


class SnippetDetails(View):
    def get(self, request, *args, **kwargs):
        snippet_id = self.kwargs["id"]
        # TODO: Implement logic to get snippet by ID
        # snippet = Snippet.objects.get(id=snippet_id)
        # Add conditions for private snippets
        return render(
            request, "snippets/snippet.html", {"snippet": snippet}
        )  # Placeholder


class UserSnippets(View):
    def get(self, request, *args, **kwargs):
        username = self.kwargs["username"]
        # TODO: Fetch user snippets based on username and public/private logic
        # snippets = Snippet.objects.filter(...)
        return render(
            request,
            "snippets/user_snippets.html",
            {"snippetUsername": username, "snippets": snippets},
        )  # Placeholder


class SnippetsByLanguage(View):
    def get(self, request, *args, **kwargs):
        language = self.kwargs["language"]
        # TODO: Fetch snippets based on language
        return render(request, "index.html", {"snippets": []})  # Placeholder


# class Login(View):
#    TODO: Implement login view logic with AuthenticationForm and login handling.

# class Logout(View):
#    TODO: Implement logout view logic.


class Index(View):
    def get(self, request, *args, **kwargs):
        # TODO: Fetch and display all public snippets
        return render(request, "index.html", {"snippets": []})  # Placeholder
