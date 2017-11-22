from django.shortcuts import render, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from django.views.generic import ListView, View, DetailView, TemplateView, UpdateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, FormView, DeleteView
from .models import Snippet, Language, Category
from .forms import SnippetForm, LanguageForm
from haystack.query import SearchQuerySet


class IndexView(ListView):
    template_name = "snippets/index.html"
    model = Snippet
    context_object_name = "snippet_list"
    paginate_by = 3

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['lang_form'] = LanguageForm

        return context


@method_decorator(login_required, name="dispatch")
class AddSnippetView(FormView):
    form_class = SnippetForm
    template_name = "snippets/add_snippet.html"
    success_url = reverse_lazy("snippets:index")
    initial = {'language': Language.objects.first()}

    def form_valid(self, form_class, *args, **kwargs):
        categories = form_class.cleaned_data['category']
        new_snippet = form_class.save(commit=False)
        new_snippet.author = self.request.user
        new_snippet.save()
        for index in categories:
            new_snippet.category.add(index)
        return super(AddSnippetView, self).form_valid(form_class, *args, **kwargs)


class SnippetDetailView(DetailView):
    model = Snippet
    template_name = "snippets/snippet_detail.html"
    context_object_name = 'snippet'


class FilterView(ListView):
    """Display snippets on the index page after the user has
    chosen to filter snippets by either language, author or Categories"""
    template_name = "snippets/index.html"
    context_object_name = "snippet_list"

    def get_queryset(self, *args, **kwargs):
        # Get the pk of the clicked object from the PATH_INFO key of the
        # META variable
        model = snip = ''
        self.md = self.request.META['PATH_INFO'].split("/")[2]
        pk = self.request.META['PATH_INFO'].split("/")[3]

        models = {'languages': Language, 'author': User, 'category': Category}
        model = models[self.md]
    
        self.qs = model.objects.filter(pk=pk).first()

        try:
            snip = self.qs.snippets.all()
        except:
            snip = self.qs.snippets_created.all()

        return snip

    def get_context_data(self, **kwargs):
        context = super(FilterView, self).get_context_data(**kwargs)
        context['md'] = self.md
        context['qs'] = self.qs

        return context


class FilterByView(ListView):
    """Filter snippets by languages, category and author"""
    template_name = "snippets/filter.html"

    def get_queryset(self, *args, **kwargs):
        # get the name of the model from the url

        md = self.request.META['PATH_INFO'].split("/")[2]
        model = self.lang = self.user = self.category = ''
        
        if md == "languages":
            model = Language
            self.lang = True
        elif md == "author":
            model = User
            self.user = True
        elif md == "category":
            model = Category
            self.category = True

        self.qs = model.objects.all()

        return self.qs

    def get_context_data(self, **kwargs):
        context = super(FilterByView, self).get_context_data(**kwargs)
        context['lang'] = self.lang
        context['user'] = self.user
        context['category'] = self.category

        return context


@method_decorator(login_required, name="dispatch")
class PersonalSnippetView(TemplateView):
    template_name = "snippets/personal_snippets.html"


@method_decorator(login_required, name='dispatch')
class SnippetUpdateView(UpdateView):
    model = Snippet
    form_class = SnippetForm
    template_name = "snippets/edit_snippet.html"


@method_decorator(login_required, name='dispatch')
class SnippetDeleteView(DeleteView):
    model = Snippet
    success_url = reverse_lazy("snippets:personal_snippets")


class SearchView(ListView):
    """A view to perform search"""
    template_name = "snippets/search.html"

    def get_queryset(self, *args, **kwargs):
        qs = Snippet.objects.all()
        self.query = self.request.GET.get("q", None)

        if self.query is not None:
            qs = qs.filter(
                Q(title__icontains=self.query) |
                Q(description__icontains=self.query) |
                Q(author__username__icontains=self.query) |
                Q(code__icontains=self.query) |
                Q(language__name__icontains=self.query))

        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(SearchView, self).get_context_data(*args, **kwargs)
        context['query'] = self.query

        return context


@method_decorator(login_required, name="dispatch")
class LanguageRegisterView(FormView):
    """Displays a form for the user to choose the languages he is
    currently working with.
    """
    form_class = LanguageForm
    http_method_names = ['post']

    def form_valid(self, form, *args, **kwargs):
        cd = form.cleaned_data
        for pk in cd['language']:
            lang = get_object_or_404(Language, pk=int(pk))
            self.request.user.languages.add(lang)

        return render(self.request, 'accounts/profile.html')
