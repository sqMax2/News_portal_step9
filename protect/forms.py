
from django import forms
from django.contrib.auth.models import User
from django.forms import formset_factory
from newsapp.models import Category


class SubscribeForm(forms.ModelForm):
    categoryChoises = [(c.id, c.name) for c in Category.objects.all()]
    # text_field = forms.CharField(label='Output', max_length=40)
    category = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=(categoryChoises),

        # initial=categorySubscription,

    )

    class Meta:
        model = User

        fields = (
            'category',
        )
