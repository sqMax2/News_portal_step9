from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    text = forms.Textarea()
    title = forms.CharField(max_length=40)

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
