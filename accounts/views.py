from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views.generic import View, UpdateView, DetailView
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from .forms import UserEditForm, ProfileEditForm
from snippets.models import Language
from snippets.forms import LanguageForm
    
    
@method_decorator(login_required, name='dispatch')
class ProfileEditView(View):
    def get(self, request, *args, **kwargs):
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'accounts/profile_edit.html', context)
    
    def post(self, request, *args, **kwargs):
        user_form = UserEditForm( instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST, files=request.FILES) 
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse_lazy('profile_view',
                args=(self.request.user.pk, self.request.user.username)))
        context = {'user_form': user_form, 'profile_form': profile_form}
        return render(request, 'accounts/profile_edit.html', context)


class ProfileView(DetailView):
    model = User
    template_name = 'accounts/profile.html'
    slug_url_kwarg = 'username'
    slug_field = 'username'
    context_object_name = 'user'

    