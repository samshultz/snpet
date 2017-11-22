from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.text import slugify


class Language(models.Model):
    name = models.CharField(max_length=50)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='languages')
    language_mode = models.CharField(max_length=50, default='')
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = 'name',


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"
        ordering = 'name',


class Snippet(models.Model):
    title = models.CharField(max_length=200)
    language = models.ForeignKey(Language, related_name='snippets')
    category = models.ManyToManyField(Category, related_name='snippets')
    slug = models.SlugField(unique_for_date='created', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               related_name="snippets_created")
    description = models.TextField(max_length=300)
    code = models.TextField()
    upvotes = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name="snippets_upvoted", blank=True)
    downvotes = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name="snippets_downvoted", blank=True)
    bookmarks = models.ManyToManyField(settings.AUTH_USER_MODEL,
        related_name="bookmarked_snippets", blank=True)
    sample_input = models.TextField(blank=True)
    sample_output = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Snippet, self).save(*args, **kwargs)
        

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("snippets:snippet_detail", args=[self.pk, self.slug])

    class Meta:
        ordering = '-created',
