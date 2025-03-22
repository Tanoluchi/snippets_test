from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from .models import Snippet
from .utils import is_the_owner

def owner_required(view_func):
    """
    Decorador para verificar si el usuario autenticado es el dueño del snippet.
    Si no es el dueño, lo redirige a la página de inicio.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        snippet = get_object_or_404(Snippet, id=kwargs["id"])
        is_owner = is_the_owner(request, snippet.user.username)
        if not is_owner:
            return redirect("index")
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view