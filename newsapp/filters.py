from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from django.forms import DateInput, CheckboxSelectMultiple
from .models import Author, Category, Post, Comment
from django.utils.translation import gettext as _


class PostFilter(FilterSet):
    # category field filter
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label=_('Category'),
        widget=CheckboxSelectMultiple(),
        # empty_label='any'
    )
    # changing default date selector to calendar view
    date_widget = DateInput()
    date_widget.input_type = 'date'
    dateCreation = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        widget=date_widget,
        label=_('Creation date since')
    )

    class Meta:
        # model
        model = Post
        # filtring fields
        fields = {
            # news title
            'title': ['icontains'],
        }

    def __init__(self, *args, **kwargs):
        super(PostFilter, self).__init__(*args, **kwargs)
        self.filters['title__icontains'].label = _('Title contains:')
