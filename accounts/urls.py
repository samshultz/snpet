from django.contrib.auth import views as auth_views
from django.conf.urls import url
from .views import ProfileEditView, ProfileView

urlpatterns = [
    
    # profile urls
    url(r'^profile_edit/$', ProfileEditView.as_view(), name="profile_edit"),
    url(r'^(?P<pk>\d+)/(?P<username>[-\w]+)/profile$',
        ProfileView.as_view(), name="profile_view"),

]
