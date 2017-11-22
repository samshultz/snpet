from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.conf import settings
from django_webtest import WebTest


class LoginFormViewTest(WebTest):
    def setUp(self):
        User.objects.create_superuser(username="samshultz", password="reductionism", email="samshultz2@hotmail.com")
        
    def test_form_display(self):
        response = self.app.get('/accounts/login/')
        self.assertEqual(len(response.forms), 1)
        
    def test_form_success(self):
        page = self.app.get('/accounts/login/')
        page.form['username'] = "samshultz"
        page.form['password'] = "reductionism"
        page = page.form.submit()
        self.assertRedirects(page, settings.LOGIN_REDIRECT_URL)
        
    def test_form_username_blank(self):
        page = self.app.get('/accounts/login/')
        page.form['username'] = ""
        page.form['password'] = "reductionism"
        page = page.form.submit()
        self.assertContains(page, "This field is required.")
    
    def test_form_password_blank(self):
        page = self.app.get('/accounts/login/')
        page.form['username'] = "samshultz"
        page.form['password'] = ""
        page = page.form.submit()
        self.assertContains(page, "This field is required.")    
    
    def test_form_blank(self):
        page = self.app.get('/accounts/login/')
        page.form['username'] = ""
        page.form['password'] = ""
        page = page.form.submit()
        self.assertContains(page, "This field is required.")
        
    def test_form_invalid_credentials(self):
        page = self.app.get('/accounts/login/')
        page.form['username'] = "samshultz"
        page.form['password'] = "reductionis"
        page = page.form.submit()
        self.assertContains(page, "Your Username and password didn't match. Please try again.")
    
class PasswordChangeFormTest(WebTest):
    def setUp(self):
        self.user = User.objects.create_superuser(username="samshultz", password="reductionism", email="samshultz2@hotmail.com")
    
    def login_credentials(self, password='reductionism'):
        login = self.app.get('/accounts/login/')
        login.form['username'] = "samshultz"
        login.form['password'] = password
        return login.form.submit()
        
    def test_form_display(self):
        self.login_credentials()
        response = self.app.get('/accounts/password/change/')
        self.assertEqual(len(response.forms), 1)
        
    def test_form_without_login(self):
        response = self.app.get('/accounts/password/change/')
        self.assertRedirects(response, settings.LOGIN_URL + "?next=/accounts/password/change/")
        
    def test_confirm_password_change(self):
        self.login_credentials()      
        response = self.app.get('/accounts/password/change/')
        response.form['old_password'] = 'reductionism'
        response.form['new_password1'] = 'recreation'
        response.form['new_password2'] = 'recreation'
        response = response.form.submit()
        
        login = self.login_credentials(password='recreation')
        
        self.assertRedirects(login, settings.LOGIN_REDIRECT_URL)
        
    def test_form_success(self):
        self.login_credentials()     
        response = self.app.get('/accounts/password/change/')
        response.form['old_password'] = 'reductionism'
        response.form['new_password1'] = 'recreation'
        response.form['new_password2'] = 'recreation'
        response = response.form.submit()
        
        self.assertRedirects(response, '/accounts/password_change/done/')

class PasswordResetTest(WebTest):
    def setUp(self):
        self.response = self.app.get('/accounts/password_reset/')
        
    def test_that_the_page_was_successfully_loaded(self):
        self.assertEqual(self.response.status_code, 200)
        
    def test_that_the_form_was_displayed(self):
        self.assertEqual(len(self.response.forms), 1)
        
    def test_form_with_valid_data(self):
        page = self.app.get('/accounts/password_reset/')
        page.form['email'] = 'samshultz2@hotmail.com'
        page = page.form.submit()
        self.assertRedirects(page, '/accounts/password_reset/done/')
        

class RegistrationFormTests(WebTest):
    def test_that_the_form_was_successfully_displayed(self):
        page = self.app.get('/accounts/register/')
        self.assertEqual(len(page.forms), 1)
    
    def test_form_with_valid_data(self):
        page = self.app.get('/accounts/register/')
        page.form['username'] = 'arthur'
        page.form['password1'] = 'reddington'
        page.form['password2'] = 'reddington'
        page = page.form.submit()
        
        login = self.app.get('/accounts/login/')
        login.form['username'] = 'arthur'
        login.form['password'] = 'reddington'
        login = login.form.submit()
        
        self.assertRedirects(login, settings.LOGIN_REDIRECT_URL)
    
    def test_that_the_correct_template_was_rendered_after_registration(self):
        page = self.app.get('/accounts/register/')
        page.form['username'] = 'arthur'
        page.form['password1'] = 'reddington'
        page.form['password2'] = 'reddington'
        page = page.form.submit()
        
        self.assertTemplateUsed('/accounts/register_done.html/')
        
class ProfileFormTest(WebTest):
    def test_that_form_was_displayed(self):
        page = self.app.get(reverse_lazy('profile_edit'))
        self.assertEqual(len(page.forms), 1)
