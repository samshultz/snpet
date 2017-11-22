from django.conf.urls import url
from .views import (
    IndexView,
    AddSnippetView,
    LanguageRegisterView,
    SnippetDetailView,
    FilterView,
    FilterByView,
    PersonalSnippetView,
    SnippetDeleteView,
    SnippetUpdateView,
    SearchView,)

app_name = "snippets"

urlpatterns = [
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^snippets/add/$', AddSnippetView.as_view(), name="add_snippet"),
    url(r'^snippets/(?P<pk>\d+)/(?P<slug>[-\w]+)/$',
        SnippetDetailView.as_view(), name='snippet_detail'),
    url(r'^snippets/personal/view/$', PersonalSnippetView.as_view(),
        name="personal_snippets"),
    url(r'^snippets/languages/$', FilterByView.as_view(), name="lang_view"),
    url(r'^snippets/languages/(?P<pk>\d+)/$',
        FilterView.as_view(), name="lang_filter"),
    url(r'^snippets/author/$', FilterByView.as_view(), name="author_view"),
    url(r'^snippets/category/$', FilterByView.as_view(), name="category_view"),
    url(r'^snippet/author/(?P<pk>\d+)/$',
        FilterView.as_view(), name="author_filter"),
    url(r'^snippet/category/(?P<pk>\d+)/$',
        FilterView.as_view(), name="category_filter"),

    url(r'^snippets/edit/(?P<pk>\d+)/$', SnippetUpdateView.as_view(), name="edit_snippet"),
    url(r'^snippets/(?P<pk>\d+)/delete$', SnippetDeleteView.as_view(),
        name="del_snippet"),
    url(r'^search/$', SearchView.as_view(), name='snippet_search'),
    url(r'^lang/reg/$', LanguageRegisterView.as_view(), name="language_register"),
    
]