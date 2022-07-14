from django.contrib.auth.models import Group
from django.views.generic import TemplateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .forms import SubscribeForm
from newsapp.models import Category
import pytz
from django.utils import timezone


class IndexView(LoginRequiredMixin, FormView):
    template_name = 'protect/index.html'
    form_class = SubscribeForm

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        current_user = self.request.user
        categorySubscription = [c.id for c in current_user.categories.all()]
        # for c in current_user.categories.all():
        #     categorySubscription.append(c.id)
        form.fields['category'].initial = categorySubscription
        return form

    def post(self, request, *args, **kwargs):
        current_url = self.request.path
        redirectURL = '/'
        form = super().get_form(form_class=self.form_class)
        form.is_valid()
        # TODO fix broken subscription
        # if form.cleaned_data:
        #     choosenOnes = list([co[0] for co in form.cleaned_data['category']])
        # else:
        #     choosenOnes = []
        choosenOnes = list([co[0] for co in form.cleaned_data['category']])
        for c in Category.objects.all():
            if str(c.id) in choosenOnes:
                c.subscribers.add(request.user)
            else:
                c.subscribers.remove(request.user)
        return redirect(redirectURL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        context.update({
            'current_time': timezone.localtime(timezone.now()),
            'timezones': pytz.common_timezones
        })
        return context


@login_required
def subscribe_me(request):
    # user = request.user
    # authors_group = Group.objects.get(name='authors')
    # if not request.user.groups.filter(name='authors').exists():
    #     authors_group.user_set.add(user)
    #     # Author.objects.create(authorUser=user)
    return redirect('/')
