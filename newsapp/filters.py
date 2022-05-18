from django_filters import FilterSet, ModelMultipleChoiceFilter, DateFilter
from django.forms import DateInput, CheckboxSelectMultiple
from .models import Author, Category, Post, Comment


class PostFilter(FilterSet):
    # category field filter
    category = ModelMultipleChoiceFilter(
        field_name='postcategory__categoryThrough',
        queryset=Category.objects.all(),
        label='Category',
        widget=CheckboxSelectMultiple()
        #empty_label='any'
    )
    # changing default date selector to calendar view
    date_widget = DateInput()
    date_widget.input_type = 'date'
    dateCreation = DateFilter(
        field_name='dateCreation',
        lookup_expr='gte',
        widget=date_widget,
    )

    class Meta:
        # model
        model = Post
        # filtring fields
        fields = {
            # news title
            'title': ['icontains'],
        }
