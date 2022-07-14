from django import forms
from django.core.exceptions import ValidationError
from .models import Post
from django.contrib.auth.models import User
from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    text = forms.Textarea()
    # text.label = _('Text')
    title = forms.CharField(max_length=40, label=_('Title'))

    class Meta:
        model = Post
        fields = [  # '__all__'
            'author',
            # 'categoryType',
            'postCategory',
            'title',
            'text',
        ]

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        text = cleaned_data.get('text')
        if text == title:
            raise ValidationError({
                '''Post text can't be the same as it's title'''
            })
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = _('Text')
        self.fields['author'].label = _('Author')
        self.fields['postCategory'].label = _('Category')



class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [  # '__all__'
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
        ]

