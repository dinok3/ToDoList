import django_filters
from django_filters import CharFilter
from .models import todolist

class todolistFilter(django_filters.FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = todolist
        exclude = ["date_created"]

