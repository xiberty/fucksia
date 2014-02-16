from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView

from fucksia.accounts.forms import CreateAccountForm
from fucksia.accounts.models import User

class CreateAccount(CreateView):
	template_name = "accounts/user_form.html"
	model = User
	success_url = reverse_lazy('login')
	form_class = CreateAccountForm
