from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from pygments import formatters, highlight, lexers
from pygments.lexers import get_all_lexers
from pygments.util import ClassNotFound


class Language(models.Model):
    LEXERS_NAMES = ((lexer[1][0], lexer[0]) for lexer in get_all_lexers() if lexer[1]) # Use a generator to reduce memory

    name = models.CharField(max_length=50, choices=LEXERS_NAMES)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    def get_lexer(self):
        try:
            return lexers.get_lexer_by_name(self.name)
        except ClassNotFound:
            # Return "text" if not found the lexer
            return lexers.get_lexer_by_name("text")

class Snippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    snippet = models.TextField()
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created",)
    
    def highlight(self):
        return highlight(self.snippet, self.language.get_lexer(), formatters.HtmlFormatter(linenos=True))