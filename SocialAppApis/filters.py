import django_filters
from .models import User
from django.db.models import Q

class UserFilter(django_filters.FilterSet):
    
    searchFor = django_filters.CharFilter(method = "filter_by_email_or_first_name")

    class Meta:
        model= User
        fields = ['email','first_name']

    def filter_by_email_or_first_name(self, queryset,_, value):
        return queryset.filter(
            Q(email__iexact = value) |
            Q(first_name__icontains = value)
        )
