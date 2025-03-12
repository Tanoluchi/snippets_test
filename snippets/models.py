from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models

from pygments import formatters, highlight, lexers


class Language(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
    
    def get_lexer(self):
        return lexers.get_lexer_by_name(self.slug)


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